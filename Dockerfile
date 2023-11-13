FROM tiangolo/uvicorn-gunicorn-fastapi:python3.10

ENV USER_NAME=app

RUN useradd -ms /bin/bash $USER_NAME
USER $USER_NAME
WORKDIR /home/$USER_NAME
ENV PATH="/home/$USER_NAME/.local/bin:${PATH}"

RUN pip install -U --user pip

ADD ./requirements.txt .
RUN pip install --upgrade --no-cache-dir -r requirements.txt

CMD ["gunicorn", "canopy_server.app:app", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:${PORT}", "--workers", "4"]
