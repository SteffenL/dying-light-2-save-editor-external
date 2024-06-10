# DL2SE External

## Building

Environment variables can be set before running scripts:

| Name                       | Value                | OS      |
| -------------------------- | -------------------- | ------- |
| `CMAKE_BUILD_TYPE`         | `Debug` or `Release` | Any     |
| `GCLOUD_BUCKET`            | gcloud bucket URI    | Any     |
| `GCLOUD_CREDENTIAL_BASE64` | (secret)             | Any     |
| `VCVARS_ARCH`              | `x64`                | Windows |
| `VCVARS_VERSION`           | `14.3`               | Windows |

Crate A virtual environment for Python:

```
python -m venv .venv
# Linux: source .venv/bin/activate
# Windows: ".venv/Scripts/activate"
pip install -r scripts/requirements.txt
```

Run the build script:

```
python scripts/devenv.py python scripts/build.py
```
