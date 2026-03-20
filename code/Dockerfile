FROM python:3.12-slim
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir google-adk
EXPOSE 8080
CMD ["adk", "web", "--host", "0.0.0.0", "--port", "8080", "."]
