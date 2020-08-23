FROM python:3.7

ENV DEBUG=0
ENV PATH="./:${PATH}"

RUN mkdir /app
COPY . /app
WORKDIR /app

RUN DEBIAN_FRONTEND=noninteractive && \
    apt-get update && \
    apt-get install -y cron && \
    pip install -r /app/requirements.txt && \
    python manage.py collectstatic --noinput

RUN mkdir -p ./database

RUN useradd -u 1000 -g 102 -d /app -M -s /bin/bash user
RUN chmod +x ./*.sh && \
    chown -R user:crontab /app && \
    chown -R user:crontab database && \
    chown -R user:crontab media && \
    chown -R user:crontab static && \
    chmod 755 /app

USER user

# RUN python manage.py migrate --noinput && \
    # python manage.py crontab remove && \
    # python manage.py crontab add && \
    # python manage.py crontab show

CMD ["entrypoint.sh"]