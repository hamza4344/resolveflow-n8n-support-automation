FROM python:3.12-slim
WORKDIR /app
COPY service /app/service
COPY knowledge /app/knowledge
RUN useradd --uid 10001 --create-home appuser && mkdir /data && chown appuser /data
USER appuser
ENV DB_PATH=/data/resolveflow.db PYTHONUNBUFFERED=1
EXPOSE 8000
CMD ["python", "-m", "service.app"]
