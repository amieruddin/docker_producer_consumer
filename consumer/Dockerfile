FROM python:3.9

WORKDIR /home/delloyd/15.tapway/consumer/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY consumer.py ./

CMD ["python", "./consumer.py"]

