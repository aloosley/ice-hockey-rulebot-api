FROM python:3.10

ADD ./requirements.txt .

RUN pip install -U pip
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

CMD ["canopy", "start"]
