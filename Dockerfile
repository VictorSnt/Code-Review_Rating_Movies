FROM python:3.11.3-alpine3.18
LABEL mantainer="victoorsantos266@gmail.com"

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
COPY api /api
COPY scripts /scripts

WORKDIR /api
EXPOSE 8000

RUN pip install --upgrade pip && \
    pip install pipenv && \
    python -m pipenv install --system && \
    adduser --disabled-password --no-create-home duser && \
    mkdir -p /data/web/static && \
    mkdir -p /data/web/media && \
    chown -R duser:duser /data/web/static && \
    chown -R duser:duser /data/web/media && \
    chmod -R 775 /data/web/static && \
    chmod -R 775 /data/web/media && \  
    chmod -R +x /scripts 

ENV PATH="/scripts:$PATH"
USER duser
CMD ["commands.sh"]
