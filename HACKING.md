# Setup

Pre-requisite: having `python3` install. 

First, create a python environment: 
```shell
python3 -m venv .env
```

Then, activate your environment: 
```shell
source .env/bin/activate
```

Download all the required packages: 
```shell
pip install -r requirements.txt
```

Alternatively, you can run:
```shell
docker build -t streamlit-app .
docker run -p 8501:8501 streamlit-app
```
