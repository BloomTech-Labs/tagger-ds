FROM python:3.7

COPY . /app

WORKDIR /app

RUN pip install pipenv
RUN pipenv install

EXPOSE 5000
CMD ["pipenv", "run", "python", "application.py"]
