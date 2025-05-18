FROM python:3.12.10-bookworm

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt ./requirements.txt

RUN pip install -r requirements.txt

COPY . .

COPY prestart.sh ./prestart.sh

RUN chmod +x ./prestart.sh

ENTRYPOINT ["/app/prestart.sh"]

CMD ["python","-m","app.main"]