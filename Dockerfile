FROM python:3.11.9-alpine3.20 as virtual-env
RUN mkdir -p /opt/packages && \
    adduser -D builder && \
    chown -R builder:builder /opt/packages
RUN apk add --no-cache \
    build-base=0.5-r3 \
    linux-headers=6.6-r0
USER builder
COPY ./requirements.txt /home/builder
RUN pip install --no-cache-dir --target /opt/packages -r /home/builder/requirements.txt

FROM python:3.11.9-alpine3.20
RUN mkdir -p /vol/web/static /vol/web/media /app/spark && \
    adduser -D spark
COPY --chown=spark:spark --from=virtual-env /opt/packages /opt/packages
COPY --chown=spark:spark ./spark ./entrypoint.sh /app/spark/
USER spark
WORKDIR /app/spark
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONPATH="/opt/packages:$PYTHONPATH"
ENV PATH="/opt/packages/bin:$PATH"
CMD ["./entrypoint.sh"]
