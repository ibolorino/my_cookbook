# Project

### Make enviroment ###
```
pyenv shell 3.9.5 &&  python -m venv .venv && source .venv/bin/activate
pip install -U pip setuptools
pip install -r requirements-dev.txt
docker-compose up -d && source .venv/bin/activate
```
## running
```
make runserver
```
### Running unit tests ###
```
make test
```
