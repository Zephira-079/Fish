@echo off

python -m venv env
cd ./env/scripts
activate
cd ../..
pip install -r requirements.txt
pyinstaller --onefile Fish.py