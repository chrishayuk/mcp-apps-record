FROM python:3.12-slim

WORKDIR /app

RUN pip install --no-cache-dir "mcp[cli]>=1.6.0" "httpx>=0.27.0" "chuk-view-schemas[fastmcp]>=0.1.0" "uvicorn>=0.34.0"

COPY simple_server.py manual_server.py decorator_server.py server.py ./

EXPOSE 8000

CMD ["python", "server.py"]
