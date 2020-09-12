FROM ubuntu:18.04
RUN apt-get update && apt-get install -y \
    unzip \
    curl \
    vim \
    git \
    dnsutils \
    wget \
    nginx \
    ca-certificates \
    python3 \
    python3-pip

ARG CONSUL_VERSION=1.8.3
ARG CONSUL_TEMPLATE_VERSION=0.20.0

RUN wget https://releases.hashicorp.com/consul/${CONSUL_VERSION}/consul_${CONSUL_VERSION}_linux_amd64.zip -O /tmp/consul.zip; unzip /tmp/consul.zip -d /usr/local/bin/; rm /tmp/consul.zip
RUN wget https://releases.hashicorp.com/consul-template/${CONSUL_TEMPLATE_VERSION}/consul-template_${CONSUL_TEMPLATE_VERSION}_linux_amd64.zip -O /tmp/consul-template.zip; unzip /tmp/consul-template.zip -d /usr/local/bin; rm /tmp/consul-template.zip
RUN mkdir /app; mkdir /consul; mkdir /consul/consul.d; mkdir /consul/data; mkdir /consul/consul-template.d; mkdir /consul/conf
COPY conf /consul/conf
COPY consul.d /consul/consul.d
COPY app.py /app
COPY requirements.txt /app
COPY entrypoint.sh .

ENTRYPOINT ["/bin/bash","/entrypoint.sh"]

CMD server