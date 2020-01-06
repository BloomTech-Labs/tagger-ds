# app/Dockerfile
# Start with a base image
FROM python:3.6
RUN pip install --upgrade pip
RUN pip install tensorflow
# Copy our application code
WORKDIR /var/app
COPY . .
COPY requirements.txt .
# Fetch app specific dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
# Expose port
EXPOSE 8000
# Start the app
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:8000"]