
````
python3 -m venv shortening_env
source ./shortening_env/bin/activate
pip3 install -r requirements.txt
PYTHONPATH=src py.test tests/
PYTHONPATH=src python3 -m shortener

```