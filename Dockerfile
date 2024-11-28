FROM python:3.12.5

WORKDIR /Text2SQL

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "/Text2SQL/main_flow.py"]

