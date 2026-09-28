# OpenCV Setup

## Requirements

- Python 3.10 or newer
- A terminal and a code editor
- About 200 MB for the Python packages

## Windows PowerShell

Run these commands from the repository root:

```powershell
cd 'OpenCv/0-Getting-Ready-With-OpenCV'
py -m venv .venv
.\.venv\Scripts\Activate.ps1
py -m pip install --upgrade pip
py -m pip install -r requirements.txt
py examples/01_check_installation.py
```

If PowerShell blocks activation, run this once for the current user, then open a new terminal:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

You can also skip activation and call `.venv\Scripts\python.exe` directly.

## macOS or Linux

```bash
cd OpenCv/0-Getting-Ready-With-OpenCV
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python examples/01_check_installation.py
```

## Verify the installation

The check script prints the installed OpenCV version and NumPy version. If it fails, confirm that the virtual environment is active and that `pip` installed into the same Python interpreter used to run the script.

```powershell
py -c "import cv2, numpy; print(cv2.__version__, numpy.__version__)"
```

## Common issues

- **`No module named cv2`**: activate `.venv`, then install `-r requirements.txt` again.
- **A window does not open**: use the file-saving examples; GUI display needs a desktop session.
- **Camera cannot be opened**: close other camera applications and check operating-system permissions. The camera example exits cleanly when no camera is available.
- **Package conflicts**: create a fresh `.venv` for this module instead of changing the system Python installation.
