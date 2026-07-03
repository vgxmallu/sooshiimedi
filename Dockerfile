
#Made-with-VGX-SHIT-THINGS

#FROM python:3.9-slim-buster
FROM python:3.11-slim-bookworm

RUN apt-get update && \
    apt-get install -y --no-install-recommends git ffmpeg && \
    rm -rf /var/lib/apt/lists/*
    
RUN pip3 install --upgrade pip

WORKDIR /sooshiimedi

RUN chmod 777 /sooshiimedi

RUN apt update && apt upgrade -y && apt install ffmpeg python3 python3-pip -y

COPY requirements.txt .
RUN pip3 install -r requirements.txt

COPY . .
CMD ["python3", "-m", "mbot"]
