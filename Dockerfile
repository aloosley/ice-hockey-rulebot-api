FROM tiangolo/uvicorn-gunicorn-fastapi:python3.11-slim

ENV USER_NAME=app

RUN useradd -ms /bin/bash $USER_NAME
USER $USER_NAME
WORKDIR /home/$USER_NAME
ENV PATH="/home/$USER_NAME/.local/bin:${PATH}"

RUN pip install -U --user pip

COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY ./pyproject.toml .
COPY ./README.md .
RUN mkdir src
COPY ./src/icehockey_rules ./src/icehockey_rules
RUN pip install --no-cache-dir -e .

COPY ./*.py ./

COPY ./data/iihf-qa.yaml ./data/iihf-qa.yaml

COPY ./config/config.yaml ./config/config.yaml

EXPOSE 8000

CMD ["gunicorn", "app:app", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000", "--workers", "2"]
