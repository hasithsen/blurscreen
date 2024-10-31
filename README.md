# blurscreen
Blur your screen as you see fit!

### Run locally

```sh
python3 -m venv .pyenv
source ./pyenv/bin/activate
pip install -i reqiurements.txt
python3 blurscreen.py
```

### Build with PyInstaller

```sh
pyinstaller blurscreen.py --hidden-import=PIL._tkinter_finder
```
