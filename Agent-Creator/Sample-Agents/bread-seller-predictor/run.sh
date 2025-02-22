
#!/bin/bash
pip install -r requirements.txt
FLASK_APP=app.py flask run --host=0.0.0.0 --port=5000
