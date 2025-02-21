# OCR Agent
This is a OCR agent

1.- Clone repository
```
git clone https://github.com/MauMontenegro/ocr-agent.git
```

2.- Set Up and activate environment
```
python -m venv venv
venv/scripts/activate
```

3.- Install requirements
```
pip install requirements.txt
```

4.- Run API. This will run Fastapi app in port 8000 on localhost. Docs can bee seen in /docs
```
python main.py
```

Can change or add languages in this line :
```
reader = easyocr.Reader(["en"],gpu=True) -> Default English
```

Create on root a folder called "uploads"
