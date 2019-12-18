FROM continuumio/miniconda3:latest
SHELL ["/bin/bash", "-c"]

ARG PYTHON_VERSION=3.6
ARG VENV=pyenv
ARG AIRFLOW_USER_HOME=/airflow
ARG AIRFLOW_VERSION=1.10.3

ENV AIRFLOW_HOME=${AIRFLOW_USER_HOME}
ENV VENV=${VENV}

RUN apt-get update
RUN apt-get install -y gcc libpthread-stubs0-dev \
        freetds-bin \
        build-essential \
        default-libmysqlclient-dev \
        apt-utils \
        curl \
        rsync \
        netcat \
        locales

RUN useradd -ms /bin/bash -d ${AIRFLOW_USER_HOME} airflow
COPY config/airflow.cfg ${AIRFLOW_USER_HOME}/airflow.cfg
RUN chown -R airflow: ${AIRFLOW_USER_HOME}

RUN conda create -n ${VENV} python=${PYTHON_VERSION}

RUN mkdir /app
COPY setup.py /app/setup.py
COPY Makefile /app
COPY README.md /app
COPY docker/entrypoint.sh /
COPY {{cookiecutter.project_slug}} /app/{{cookiecutter.project_slug}}
COPY airflow /app/airflow
COPY scripts /app/scripts
COPY tests /app/tests

RUN chmod +x /entrypoint.sh

WORKDIR /app
RUN git config --global user.email "{{cookiecutter.project_slug}}"
RUN git config --global user.name "{{cookiecutter.project_slug}}"
RUN make configure
RUN source /opt/conda/bin/activate ${VENV} && make requirements

USER airflow
WORKDIR ${AIRFLOW_USER_HOME}
ENTRYPOINT ["/entrypoint.sh"]
CMD ["webserver"]
