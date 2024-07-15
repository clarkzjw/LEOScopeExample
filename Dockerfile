FROM python:3.12.2-slim-bullseye

RUN apt-get update && apt-get install wget curl iputils-ping mtr traceroute dnsutils gnuplot zstd chrony git swaks procps nano -y

RUN pip install poetry

WORKDIR /leotest/leotest

RUN wget https://github.com/fullstorydev/grpcurl/releases/download/v1.9.1/grpcurl_1.9.1_linux_amd64.deb && \
    dpkg -i grpcurl_1.9.1_linux_amd64.deb && \
    rm grpcurl_1.9.1_linux_amd64.deb 

RUN git clone https://github.com/sparky8512/starlink-grpc-tools.git

ADD poetry.lock .
ADD pyproject.toml .

RUN poetry install

ADD . /leotest/leotest

WORKDIR /leotest

CMD ["poetry", "-C", "leotest", "run", "python", "-m", "leotest", "--test-config", "/artifacts/experiment-config.yaml"]
