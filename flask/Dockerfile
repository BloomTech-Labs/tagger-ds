# Choose what version of python to base you image on.
# Using :latest did not have any dependancy issues for these packages; try :3.7.6 if the packages don't like python 3.8
# FROM python:3.7.6-buster
FROM python:latest

# Most guides recommend updating the Kernel before installing anything else
# Proceed to install the necessary packages, (example: TensorFlow..) that needs to install outside of pip
RUN apt-get update \
    && apt-get install -qq -y build-essential libpq-dev python3-setuptools --no-install-recommends

# THe following makes the directory within the container that will house the flask API specifically
ENV INSTALL_PATH /flask
RUN mkdir $INSTALL_PATH
WORKDIR $INSTALL_PATH

# this line is supposed to improve performance of python inside a container whne running an API.
ENV PYTHONUNBUFFERED 1

# This is another way of installing packages. It was not tried in LABS20.
# WORKDIR /  
# COPY requirements.txt ./  
# RUN pip install --no-cache-dir -r requirements.txt  
# RUN rm requirements.txt

# This tells pip3 to install the packages the Flask container will need.
RUN python3 -m pip install --no-binary :all: psycopg2 && \
    python3 -m pip install Flask Flask_SQLAlchemy \
    scikit-learn beautifulsoup4 \
    numpy python-decouple click \
    python-dotenv requests psycopg2-binary \
    lxml pandas basilica gunicorn celery Flask_celery

# This line will copy everything inside /flask into a folder called flask inside the container.
COPY . .

# This line will install the cli that is needed to run to initiate the database.
RUN pip install --editable .

# This CMD will run gunicorn with the configuration that is set by /flask/config.
# important to note that EC2 only allows HTTP through port :80.
CMD gunicorn -c "python:config.gunicorn" "tagger:APP"