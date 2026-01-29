install:
	pip install -r requirements.txt

test:
	export PYTHONPATH=$PYTHONPATH:. && pytest

run:
	export API_KEY=dev-key && python -m src.app

clean:
	rm -rf __pycache__
	rm -rf src/__pycache__
	rm -rf tests/__pycache__
