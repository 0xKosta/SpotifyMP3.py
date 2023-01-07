set +v
echo Installing necessary requirements.
pip install -r requirements.txt --quiet
echo Requirements installed, starting app...
python main.py
