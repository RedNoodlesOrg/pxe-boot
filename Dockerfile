FROM python:3.13-slim

ARG VCS_REF=unknown
ARG BUILD_DATE=unknown

LABEL org.opencontainers.image.title="PXE Api"
LABEL org.opencontainers.image.description="API service for PXE boot provisioning"
LABEL org.opencontainers.image.version="1.0.0"
LABEL org.opencontainers.image.revision="${VCS_REF}"
LABEL org.opencontainers.image.created="${BUILD_DATE}"


ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update && \
    apt-get install -y \
    --no-install-recommends curl && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY ./requirements.txt /tmp/requirements.txt

RUN pip install --no-cache-dir --upgrade \
    -r /tmp/requirements.txt \
    --root-user-action ignore && \
    rm /tmp/requirements.txt

COPY ./src/app /app

# Non-root user
RUN useradd -r -u 10001 -g users appuser \
 && mkdir -p /profiles /artifacts \
 && chown -R appuser:users /app /profiles /artifacts
USER appuser

EXPOSE 8080

VOLUME [ "/profiles", "/artifacts" ] 

HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD [ "curl", "--include", "--request", "GET", "http://localhost:8080/healthcheck" ]

CMD ["fastapi", "run", "/app/main.py","--proxy-headers", "--port", "8080", "--host", "0.0.0.0"]
