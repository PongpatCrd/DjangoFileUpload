FROM python:3.7-slim

ENV TZ=Asia/Bangkok
ENV PATH="/app/:${PATH}"

RUN mkdir /app
COPY . /app

RUN pip install -r /app/requirements.txt

WORKDIR /app/send
RUN mkdir -p ./database
RUN mkdir -p ./media
RUN mkdir -p ./static

RUN useradd -u 1000 -d /app -M -s /bin/bash user && \
    chmod +x /app/*.sh && \
    chown -R user:user /app && \
    chown -R user:user database && \
    chown -R user:user media && \
    chown -R user:user static && \
    chmod 755 /app

USER user

CMD ["entrypoint.sh"]
