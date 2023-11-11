FROM python:3.10

RUN adduser -D myuser
USER myuser
RUN pip install -U pip

ADD ./requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

CMD ["canopy", "start"]
