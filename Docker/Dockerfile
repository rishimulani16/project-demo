FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app
COPY data ./data
COPY .env .env

# Expose both ports
EXPOSE 8000
EXPOSE 8501

# Use a shell script to run both services
CMD ["sh", "-c", "uvicorn app.api.main:app --host 0.0.0.0 --port 8000 & streamlit run app/frontend/streamlit_app.py --server.port 8501 --server.address 0.0.0.0"]