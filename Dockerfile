FROM python:3
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
CMD ["python3","daily_work.py"]
