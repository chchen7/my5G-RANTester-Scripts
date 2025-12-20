# Use Ubuntu 22.04 as the base image
FROM ubuntu:22.04

# Update the package lists and install the desired network tools
RUN apt-get update && apt-get install -y \
    iputils-ping \
    iproute2 \
    tcpdump \
    traceroute \
    dnsutils \
    curl \
    wget

# Set the default command to run when the container starts
# This keeps the container running so you can interact with it
CMD ["bash"]