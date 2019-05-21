FROM python:3.5-alpine

ENV APP_DIR=/flask-app

EXPOSE 8080

# App configuration
WORKDIR ${APP_DIR}
RUN mkdir -p ${APP_DIR}
COPY requirements.txt ${APP_DIR}/

RUN pip install --upgrade pip && \
    pip install -U -r requirements.txt && \
    mkdir -p ${APP_DIR}/templates

COPY app.py ${APP_DIR}/
COPY index.html ${APP_DIR}/templates

ENTRYPOINT ["python"]
CMD ["app.py", "--log-file", "-"]
