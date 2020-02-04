FROM python

RUN apt-get update -q && \
    apt-get upgrade -q -y && \
    apt-get install -q -y emacs wget bzip2 sudo \
    build-essential python3-psycopg2

RUN cp /etc/apt/sources.list /etc/apt/sources.list~ && \
    sed -Ei 's/^# deb-src /deb-src /' /etc/apt/sources.list && \
    apt-get update -q && \
    DEBIAN_FRONTEND=noninteractive apt-get build-dep python3-psycopg2 -y -q

RUN apt-get update -q && \
    adduser --disabled-password --gecos '' ubuntu && adduser ubuntu sudo && \
    echo '%sudo ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers

USER ubuntu
WORKDIR /home/ubuntu/
RUN chmod 777 /home/ubuntu/ && mkdir app

RUN wget https://repo.continuum.io/archive/Anaconda3-2019.10-Linux-x86_64.sh -q && \
    bash Anaconda3-2019.10-Linux-x86_64.sh -b > /dev/null && \
    rm Anaconda3-2019.10-Linux-x86_64.sh

ENV PATH /home/ubuntu/anaconda3/bin:$PATH
ENV PYTHONUNBUFFERED 1

RUN conda init bash && \
    /bin/bash -c ". activate" && \
    conda config -q --append channels conda-forge

RUN conda install -q -y libiconv PyYAML
RUN python3 -m pip install --no-binary :all: psycopg2 && \
    python3 -m pip install pyuwsgi Flask==1.1.1 Flask_SQLAlchemy==2.4.1 \
    scikit-learn beautifulsoup4==4.8.1 \
    numpy==1.17.4 python_decouple==3.3 click\
    python_dotenv==0.10.3 requests==2.22.0 psycopg2-binary==2.8.4 \
    lxml==4.4.2 pandas==0.25.3 basilica

COPY . /home/ubuntu/

RUN pip install --editable .

CMD [ "uwsgi", "app.ini" ]