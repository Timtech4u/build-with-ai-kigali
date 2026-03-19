FROM python:3.12-slim
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir google-adk
EXPOSE 8080
CMD ["adk", "api_server", "--port", "8080", "kigali_agent"]
