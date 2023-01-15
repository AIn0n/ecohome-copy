run:
	uvicorn main:app --reload

precommit:
	pip freeze > requirements.txt
	black .
	
req:
	pip install -r requirements.txt

	