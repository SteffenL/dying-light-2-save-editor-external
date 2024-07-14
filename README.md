# DL2SE External

## Building

Environment variables can be set before running scripts:

| Name                       | Value                | OS      |
| -------------------------- | -------------------- | ------- |
| `OUTPUT_DIR`               | Build output dir     | Any     |
| `CMAKE_BUILD_TYPE`         | `Debug` or `Release` | Any     |
| `CMAKE_TOOLCHAIN_FILE`     | CMake toolchain file | Any     |
| `GCLOUD_BUCKET`            | gcloud bucket URI    | Any     |
| `TARGET_SYSTEM`            | `platform.system()`  | Any     |
| `TARGET_ARCH`              | `platform.machine()` | Any     |
| `GCLOUD_CREDENTIAL_BASE64` | (secret)             | Any     |
| `VCVARS_ARCH`              | `x64`                | Windows |
| `VCVARS_VERSION`           | `14.3`               | Windows |

Authentication for private libraries:

```
gcloud auth login --cred-file=<credentials.json> --no-launch-browser
```

set(PRIVATE_LIBS_URL gs://langnes-build-resources/libraries)

Build on Linux:

```
python -m venv .venv
source .venv/bin/activate
pip install -r scripts/requirements.txt

OUTPUT_DIR=${PWD}/output/linux python scripts/build.py
TARGET_SYSTEM=Windows TARGET_ARCH=x86_64 OUTPUT_DIR=${PWD}/output/windows CMAKE_TOOLCHAIN_FILE=${PWD}/cmake/toolchains/x86_64-w64-mingw32.cmake python scripts/build.py
```

Build on Windows:

```
python -m venv .venv
call .venv\Scripts\activate.bat
pip install -r scripts/requirements.txt

python scripts/devenv.py python scripts/build.py
```

```
cmake -G Ninja -B build -S .
cmake --install build --prefix install
```
