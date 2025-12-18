# Variables
REPO_URL=https://github.com/James-Lu-none/free5gc-compose.git
DIR_NAME=free5gc-compose

.PHONY: all clone

all: clone

clone:
	@if [ ! -d "$(DIR_NAME)" ]; then \
		echo "[INFO] Cloning repository..."; \
		git clone $(REPO_URL); \
		echo "[INFO] Patching Dockerfile in base/ ..."; \
		cd $(DIR_NAME)/base && \
		sed -i '6a \
	RUN echo "deb http://archive.debian.org/debian stretch main" > /etc/apt/sources.list && \\\
	    echo "deb http://archive.debian.org/debian-security stretch/updates main" >> /etc/apt/sources.list && \\\
	    sed -i '\''s|http://deb.debian.org|http://archive.debian.org|g'\'' /etc/apt/sources.list' Dockerfile; \
		echo "[INFO] Patch applied successfully."; \
		cd .. &&make base; \
	else \
		echo "[INFO] Repository already cloned."; \
	fi