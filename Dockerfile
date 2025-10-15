FROM ubuntu:24.04

ARG DEBIAN_FRONTEND=noninteractive
ARG PYTHON_VERSIONS="3.14 3.13 3.12 3.11 3.10 3.9"

ENV TZ=Etc/GMT
ENV PATH="$PATH:/root/.local/bin"
ENV NOX_DEFAULT_VENV_BACKEND=uv

COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv
COPY . /google-ads-python

RUN uv python install ${PYTHON_VERSIONS} && \
    uv tool install nox[uv]

RUN apt-get update -qy && \
    apt-get upgrade -qy && \
    apt-get install -qy --no-install-recommends \
        ca-certificates \
        curl \
        gnupg2 \
        git \
        openssh-client

WORKDIR "/google-ads-python"