FROM gcr.io/paradigmxyz/ctf/eth-challenge:latest

USER root
ENV HTTP_PORT=8545

RUN adduser ctf
COPY requirements.txt /root
RUN apt-get update && apt-get install -y \
    build-essential \
    socat
RUN python3 -m pip install --user cytoolz
RUN python3 -m pip install -r /root/requirements.txt 

RUN true \
    && curl -L https://foundry.paradigm.xyz | bash \
    && bash -c "source /root/.bashrc && foundryup" \
    && chmod 755 -R /root \
    && true

COPY ./98-start-gunicorn /startup
RUN mkdir /var/log/ctf
RUN chown ctf:ctf /var/log/ctf
RUN chown ctf:ctf /startup
RUN chmod +x /startup

COPY eth_sandbox /usr/lib/python/eth_sandbox
RUN chown -R ctf:ctf /usr/lib/python/eth_sandbox

ENV PYTHONPATH /usr/lib/python

COPY deploy/ /home/ctf/

COPY contracts /home/ctf/contracts

RUN true \
    && cd /home/ctf \
    && /opt/foundry/bin/forge build --out /home/ctf/compiled \
    && true

CMD ["/startup"]
