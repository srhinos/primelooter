FROM python:3.11

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY primelooter.py primelooter.py
CMD [ "python", "primelooter.py" , "--loop" ]