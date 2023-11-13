FROM python:3.10

ENV USER_NAME=app

RUN useradd -ms /bin/bash $USER_NAME
USER $USER_NAME
WORKDIR /home/$USER_NAME
ENV PATH="/home/$USER_NAME/.local/bin:${PATH}"

RUN pip install -U --user pip

ADD ./requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

EXPOSE 8000

CMD ["canopy", "start"]
