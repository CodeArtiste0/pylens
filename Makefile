install:
	python3 -m venv venv
	./venv/bin/python3 -m pip install pip --upgrade
	./venv/bin/python3 -m pip install -r requirements.txt
run:
	./venv/bin/python3 app.py
