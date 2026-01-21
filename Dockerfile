FROM python:3.11-slim

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

# copy all project files into the image workdir
COPY . .

ENV PYTHONUNBUFFERED=1

# run the FastAPI app from main.py
# CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

CMD sh -c "uvicorn main:app --host 0.0.0.0 --port ${PORT:-8080}"
