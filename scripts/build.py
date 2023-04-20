import base64
from dataclasses import dataclass
import hashlib
import json
import os
import platform
import shutil
import subprocess
import sys
from typing import Callable, List
from urllib.request import urlretrieve
from urllib.parse import urlsplit

from google.cloud import storage
import patch_ng


@dataclass
class Target:
    name: str
    version: str
    sha256: str
    filename: str
    source_subdir:  str
    url: str
    configure_options: List[str]
    download: Callable[["Target"], None] = None
    source: Callable[["Target"], None] = None
    patch: Callable[["Target"], None] = None
    configure: Callable[["Target"], None] = None
    build: Callable[["Target"], None] = None
    install: Callable[["Target"], None] = None


def sha256sum_file(file_path: str):
    with open(file_path, "rb", buffering=0) as f:
        hash = hashlib.sha256()
        while True:
            buffer = f.read(4096)
            if len(buffer) == 0:
                break
            hash.update(buffer)
        return hash.hexdigest()


def expand_target_vars(target: Target, var: str, depth: int = 1):
    if depth > 10:
        raise Exception("Possible infinite recursion")
    replaced = var.format(
        bucket=os.getenv("GCLOUD_BUCKET"),
        filename=target.filename,
        name=target.name,
        version=target.version,
    )
    if "{" in replaced:
        return expand_target_vars(target, replaced, depth + 1)
    return replaced


def create_empty_file(file_path: str):
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    open(file_path, "w").close()


ROOT_DIR = os.getcwd()
BUILD_ROOT_DIR = os.path.join(ROOT_DIR, "build")
DOWNLOAD_ROOT_DIR = os.path.join(ROOT_DIR, "download")
INSTALL_ROOT_DIR = os.path.join(ROOT_DIR, "install")
PATCH_ROOT_DIR = os.path.join(ROOT_DIR, "patch")
SOURCE_ROOT_DIR = os.path.join(ROOT_DIR, "source")


def get_download_file_path(target: Target):
    filename = expand_target_vars(target, target.filename)
    return os.path.join(DOWNLOAD_ROOT_DIR,
                        target.name, target.version, filename)


def get_source_extract_dir(target: Target):
    return os.path.join(SOURCE_ROOT_DIR, target.name, target.version)


def install_steamworks(target: Target):
    build_dir = os.path.join(BUILD_ROOT_DIR, target.name, target.version)
    if os.path.exists(build_dir + ".install.ok"):
        return
    print("Installing {} {}...".format(target.name, target.version))
    source_dir = os.path.join(
        get_source_extract_dir(target), target.source_subdir)
    # Copy header files
    source_include_dir = os.path.join(source_dir, "public", "steam")
    source_header_files = [p for p in os.listdir(
        source_include_dir) if p.endswith(".h")]
    install_include_dir = os.path.join(INSTALL_ROOT_DIR, "include", "steam")
    os.makedirs(install_include_dir, exist_ok=True)
    for file_name in source_header_files:
        shutil.copyfile(os.path.join(source_include_dir, file_name),
                        os.path.join(install_include_dir, file_name))
    # Copy library files
    source_lib_dir = os.path.join(source_dir, "redistributable_bin")
    install_runtime_lib_dir = os.path.join(
        INSTALL_ROOT_DIR, "bin" if platform.system() == "Windows" else "lib")
    install_link_lib_dir = os.path.join(INSTALL_ROOT_DIR, "lib")
    os.makedirs(install_runtime_lib_dir, exist_ok=True)
    os.makedirs(install_link_lib_dir, exist_ok=True)
    machine = platform.machine()
    if platform.system() == "Darwin":
        shutil.copyfile(os.path.join(source_lib_dir, "osx", "libsteam_api.dylib"),
                        os.path.join(install_runtime_lib_dir, "libsteam_api.dylib"))
    elif platform.system() == "Linux":
        bits = 64 if machine.lower() in ("amd64", "x86_64") else 32
        shutil.copyfile(os.path.join(source_lib_dir, "linux" + str(bits), "libsteam_api.so"),
                        os.path.join(install_runtime_lib_dir, "libsteam_api.so"))
    elif platform.system() == "Windows":
        if machine.lower() in ("amd64", "x86_64"):
            shutil.copyfile(os.path.join(source_lib_dir, "win64", "steam_api64.dll"),
                            os.path.join(install_runtime_lib_dir, "steam_api64.dll"))
            shutil.copyfile(os.path.join(source_lib_dir, "win64", "steam_api64.lib"),
                            os.path.join(install_link_lib_dir, "steam_api64.lib"))
        else:
            shutil.copyfile(os.path.join(source_lib_dir, "steam_api64.dll"),
                            os.path.join(install_runtime_lib_dir, "steam_api64.dll"))
            shutil.copyfile(os.path.join(source_lib_dir, "steam_api64.lib"),
                            os.path.join(install_link_lib_dir, "steam_api64.lib"))
    create_empty_file(build_dir + ".install.ok")


def gcloud_download(url: str, file_path: str):
    parts = urlsplit(url)
    if parts.scheme != "gs":
        raise Exception("Unsupported scheme: {}".format(parts.scheme))
    credential_base64 = os.environ["GCLOUD_CREDENTIAL_BASE64"]
    client = storage.Client.from_service_account_info(
        json.loads(base64.b64decode(credential_base64)))
    bucket = client.bucket(parts.netloc)
    path = parts.path[1:]
    bucket.blob(path).download_to_filename(file_path)


def download(target: Target):
    if target.download == False:
        return
    if target.download:
        return target.download(target)
    url = expand_target_vars(target, target.url)
    file_path = get_download_file_path(target)
    if os.path.exists(file_path + ".ok"):
        return
    print("Downloading {} {} from {}...".format(
        target.name, target.version, url))
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    if url.startswith("gs://"):
        gcloud_download(url, file_path)
    else:
        urlretrieve(url, file_path)
    digest = sha256sum_file(file_path)
    if (digest != target.sha256):
        raise Exception("Verification failed: {}".format(file_path))
    create_empty_file(file_path + ".ok")


def source(target: Target):
    if target.source == False:
        return
    if target.source:
        return target.source(target)
    extract_dir = get_source_extract_dir(target)
    if os.path.exists(extract_dir + ".extract.ok"):
        return
    print("Extracting {} {} sources...".format(target.name, target.version))
    file_path = get_download_file_path(target)
    shutil.unpack_archive(file_path, extract_dir)
    create_empty_file(extract_dir + ".extract.ok")


def patch(target: Target):
    if target.patch == False:
        return
    if target.patch:
        return target.patch(target)
    patch_file_path = os.path.join(
        PATCH_ROOT_DIR, target.name + "_" + target.version + ".patch")
    if not os.path.isfile(patch_file_path):
        return
    extract_dir = get_source_extract_dir(target)
    if os.path.exists(extract_dir + ".patch.ok"):
        return
    print("Patching {} {} sources...".format(target.name, target.version))
    subdir = expand_target_vars(target, target.source_subdir)
    source_dir = os.path.join(extract_dir, subdir) if subdir else extract_dir
    p = patch_ng.fromfile(patch_file_path)
    p.apply(strip=0, root=source_dir)
    create_empty_file(extract_dir + ".patch.ok")


def configure(target: Target):
    if target.configure == False:
        return
    if target.configure:
        return target.configure(target)
    extract_dir = get_source_extract_dir(target)
    source_dir = os.path.join(
        extract_dir, expand_target_vars(target, target.source_subdir))
    build_dir = os.path.join(BUILD_ROOT_DIR, target.name, target.version)
    if os.path.exists(build_dir + ".configure.ok"):
        return
    print("Configuring {} {}...".format(target.name, target.version))
    install_dir = INSTALL_ROOT_DIR
    subprocess.check_call((
        "cmake",
        "-G",
        "Ninja",
        "-B",
        build_dir,
        "-S",
        source_dir,
        "-DBoost_USE_STATIC_LIBS=ON",
        "-DBUILD_SHARED_LIBS=OFF",
        "-DCMAKE_BUILD_TYPE=" + os.getenv("CMAKE_BUILD_TYPE", "Release"),
        "-DCMAKE_FIND_PACKAGE_PREFER_CONFIG=TRUE",
        "-DCMAKE_INSTALL_PREFIX=" + install_dir,
        "-DCMAKE_PREFIX_PATH=" + install_dir,
        "-DPKG_CONFIG_USE_CMAKE_PREFIX_PATH=TRUE",
        "-DZLIB_USE_STATIC_LIBS=ON",
        *target.configure_options
    ))
    create_empty_file(build_dir + ".configure.ok")


def build(target: Target):
    if target.build == False:
        return
    if target.build:
        return target.build(target)
    build_dir = os.path.join(BUILD_ROOT_DIR, target.name, target.version)
    if os.path.exists(build_dir + ".build.ok"):
        return
    print("Building {} {}...".format(target.name, target.version))
    subprocess.check_call((
        "cmake",
        "--build",
        build_dir
    ))
    create_empty_file(build_dir + ".build.ok")


def install(target: Target):
    if target.install == False:
        return
    if target.install:
        return target.install(target)
    build_dir = os.path.join(BUILD_ROOT_DIR, target.name, target.version)
    if os.path.exists(build_dir + ".install.ok"):
        return
    print("Installing {} {}...".format(target.name, target.version))
    subprocess.check_call((
        "cmake",
        "--install",
        build_dir
    ))
    create_empty_file(build_dir + ".install.ok")


def copy_lib_to_install():
    print("Copying lib directory into install directory...")
    os.makedirs(INSTALL_ROOT_DIR, exist_ok=True)
    shutil.copytree(os.path.join(ROOT_DIR, "lib"),
                    os.path.join(INSTALL_ROOT_DIR, "lib"), dirs_exist_ok=True)


TARGETS = (
    Target(name="zlib",
           version="1.2.13",
           sha256="d14c38e313afc35a9a8760dadf26042f51ea0f5d154b0630a31da0540107fb98",
           filename="zlib-{version}.tar.xz",
           source_subdir="zlib-{version}",
           url="https://www.zlib.net/{filename}",
           configure_options=()),
    Target(name="boost",
           version="1.81.0",
           sha256="06bc525a392650eb6248f40a13f40112b6c485eec7103b6dcde7196f2a3570e0",
           filename="boost-{version}.tar.xz",
           source_subdir="boost-{version}",
           url="https://github.com/boostorg/boost/releases/download/boost-{version}/{filename}",
           configure_options=()),
    Target(name="cereal",
           version="1.3.2",
           sha256="16a7ad9b31ba5880dac55d62b5d6f243c3ebc8d46a3514149e56b5e7ea81f85f",
           filename="v{version}.tar.gz",
           source_subdir="cereal-{version}",
           url="https://github.com/USCiLab/cereal/archive/refs/tags/{filename}",
           configure_options=(
               "-DBUILD_TESTS=OFF",
               "-DBUILD_DOC=OFF",
               "-DBUILD_SANDBOX=OFF",
               "-DSKIP_PERFORMANCE_COMPARISON=ON",
           )),
    Target(name="msgpack",
           version="6.0.0",
           sha256="0948d2db98245fb97b9721cfbc3e44c1b832e3ce3b8cfd7485adc368dc084d14",
           filename="msgpack-cxx-{version}.tar.gz",
           source_subdir="msgpack-cxx-{version}",
           url="https://github.com/msgpack/msgpack-c/releases/download/cpp-{version}/{filename}",
           configure_options=(
                "-DMSGPACK_CXX20=ON",
                "-DMSGPACK_BUILD_DOCS=OFF",
                "-DMSGPACK_USE_BOOST=OFF",
           )),
    Target(name="wxwidgets",
           version="3.2.2.1",
           sha256="dffcb6be71296fff4b7f8840eb1b510178f57aa2eb236b20da41182009242c02",
           filename="wxWidgets-{version}.tar.bz2",
           source_subdir="wxWidgets-{version}",
           url="https://github.com/wxWidgets/wxWidgets/releases/download/v{version}/{filename}",
           configure_options=(
               "-DwxBUILD_SHARED=OFF",
           )),
    Target(name="steamworks-sdk",
           version="1.55",
           sha256="3d5ab5d2b5538fdbe49fd81abf3b6bc6c18b91bcc6a0fecd4122f22b243ee704",
           filename="steamworks_sdk_155.zip",
           source_subdir="sdk",
           url="gs://{bucket}/libraries/steamworks-sdk/steamworks_sdk_155.zip",
           configure_options=(),
           configure=False,
           build=False,
           install=install_steamworks),
)

STAGES = (download, source, patch, configure, build, install)


def main(args: List[str]):
    known_target_names = set([target.name for target in TARGETS])
    for target_name in args:
        if not target_name in known_target_names:
            raise Exception("Unknown target: {}".format(target_name))
    copy_lib_to_install()
    for target in TARGETS:
        for stage in STAGES:
            if len(args) == 0 or target.name in args:
                stage(target)


if __name__ == "__main__":
    main(sys.argv[1:])
