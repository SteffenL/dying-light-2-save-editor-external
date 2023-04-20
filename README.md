# DL2SE External

## Building

On Windows you should set the `VCVARS_ARCH` and `VCVARS_VERSION` environment variables:

| Name             | Value  |
| ---------------- | ------ |
| `VCVARS_ARCH`    | `x64`  |
| `VCVARS_VERSION` | `14.3` |

Crate A virtual environment for Python:

```
python -m venv .venv
".venv/Scripts/activate"
pip install -r scripts/requirements.txt
```

Run the build script:

```
python scripts/devenv.py python scripts/build.py
```
