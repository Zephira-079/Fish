python -m venv env
cd ./env/Scripts
call activate.bat
cd ../..
pip install -r requirements.txt
pyinstaller --onefile Fish.py