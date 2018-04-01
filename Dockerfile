FROM python:3.6
# Create app directory
WORKDIR /app

# Install app dependencies
COPY requirements.txt ./

RUN pip install -r requirements.txt
RUN pip install gunicorn

EXPOSE 9001
CMD ["gunicorn", "--bind", "0.0.0.0:9001", "--error-logfile", "-", "--access-logfile", "-", "--log-level", "debug", "--workers", "3", "--worker-class", "gthread", "main:app"]
