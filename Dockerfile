```dockerfile
FROM python:3.10-slim-bullseye

# Paigaldame Go ja süsteemi tööriistad
ENV GO_VERSION=1.21.5
ENV GOPATH=/root/go
ENV PATH=$PATH:/usr/local/go/bin:$GOPATH/bin

RUN apt-get update && apt-get install -y \
    wget git curl gcc make nmap \
    && rm -rf /var/lib/apt/lists/*

RUN wget https://go.dev/dl/go${GO_VERSION}.linux-amd64.tar.gz \
    && tar -C /usr/local -xzf go${GO_VERSION}.linux-amd64.tar.gz \
    && rm go${GO_VERSION}.linux-amd64.tar.gz

# Bug Bounty tööriistade paigaldus
RUN go install -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest && \
    go install -v github.com/projectdiscovery/httpx/cmd/httpx@latest && \
    go install -v github.com/projectdiscovery/nuclei/v3/cmd/nuclei@latest && \
    go install -v github.com/projectdiscovery/katana/cmd/katana@latest && \
    go install -v github.com/hahwul/dalfox/v2@latest

# Seadistame töökeskkonna
WORKDIR /home/coder/project
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Kopeerime koodi
COPY . .

# Eksponeerime pordi
EXPOSE 5000

# Käivitame veebi, mis omakorda käivitab skanneri
CMD ["python3", "veeb.py"]

```
