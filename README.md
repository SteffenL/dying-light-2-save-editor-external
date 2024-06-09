# DL2SE External

## Building

Environment variables should be set before running scripts:

| Name                       | Value    | OS      |
| -------------------------- | -------- | ------- |
| `GCLOUD_CREDENTIAL_BASE64` | (secret) | All     |
| `VCVARS_ARCH`              | `x64`    | Windows |
| `VCVARS_VERSION`           | `14.3`   | Windows |

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
