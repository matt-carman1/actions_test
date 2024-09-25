ARG TARGET

FROM selenium/node-chrome:4.8.3-20230404 as chrome
FROM selenium/node-firefox:4.8.3-20230404 as firefox

FROM ${TARGET}
USER root
RUN apt-get update \
    && apt-get install -y \
        apt-transport-https \
        build-essential \
        ca-certificates \
        coreutils \
        curl \
        gcc \
        gnupg \
        libcairo2 \
        libffi-dev \
        libgdk-pixbuf2.0-0 \
        libpango-1.0-0 \
        libpangocairo-1.0-0 \
        python3-cffi \
        python3-dev \
        python3-pip \
        python3-setuptools \
        python3-wheel \
        shared-mime-info \
        xvfb \
    && rm -rf /var/lib/apt/lists/*

# Use UID 1000 to match jenkins user in inbound-agent image
# https://plugins.jenkins.io/kubernetes/#plugin-content-pipeline-sh-step-hangs-when-multiple-containers-are-used
RUN usermod --uid 1000 seluser

USER seluser
WORKDIR /ld-webtests
COPY requirements.txt .
RUN pip3 install -r requirements.txt
