FROM python:3.11-slim

RUN pip install --no-cache-dir flask ruamel.yaml

WORKDIR /app
COPY webapp.py /app/

EXPOSE 5000
CMD ["python", "webapp.py"]
