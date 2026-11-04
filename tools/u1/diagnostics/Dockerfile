# Extend the existing Orca build image; these are test/debug tools, not application dependencies.
ARG U1_BASE_IMAGE=ubuntu:24.04
FROM ${U1_BASE_IMAGE}
RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends gdb xvfb xauth \
    && rm -rf /var/lib/apt/lists/*
