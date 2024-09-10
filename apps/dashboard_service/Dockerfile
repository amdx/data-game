FROM python:3.12.2-slim-bookworm

RUN python -mvenv /opt/venv
ENV PATH=/opt/venv/bin:${PATH}

WORKDIR /opt/dashboard_service

COPY requirements.txt .
RUN pip \
     --disable-pip-version-check \
    install \
    --no-cache-dir \
    -r requirements.txt

COPY dashboard_service dashboard_service/

EXPOSE 6384/tcp

CMD ["uvicorn", "dashboard_service.main:app", "--host", "0.0.0.0", "--port", "6384"]
