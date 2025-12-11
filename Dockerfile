FROM python:3.11
LABEL authors="Shebik"

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# RUN alembic revision --autogenerate -m "Init"
RUN alembic upgrade head

CMD ["python", "start_bots.py"]
