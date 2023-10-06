FROM ubuntu:latest AS base
LABEL authors="guy_strauss"
RUN apt-get -y update
RUN apt-get install -y software-properties-common
RUN add-apt-repository -y ppa:deadsnakes/ppa
RUN apt-get install -y python3.10
RUN apt-get install -y python3-pip
RUN apt-get install -y gnupg curl
RUN curl -fsSL https://pgp.mongodb.com/server-7.0.asc | \
    gpg -o /usr/share/keyrings/mongodb-server-7.0.gpg \
   --dearmor
RUN echo "deb [ arch=amd64,arm64 signed-by=/usr/share/keyrings/mongodb-server-7.0.gpg ] https://repo.mongodb.org/apt/ubuntu jammy/mongodb-org/7.0 multiverse" | \
    tee /etc/apt/sources.list.d/mongodb-org-7.0.list
RUN apt-get -y update
RUN apt-get install -y mongodb-org
RUN systemctl start mongod
COPY backend /backend
COPY protos /backend/protos
COPY requirements.txt /backend/requirements.txt
WORKDIR /backend
RUN python3.10 -m pip install -r requirements.txt
EXPOSE 50051

FROM base AS production
CMD ["python3.10", "file_sync_servicer.py"]

FROM base AS test_storage
CMD ["python3.10", "-m", "unittest", "tests/test_storage.py"]

FROM base AS test_metadata
CMD ["python3.10", "-m", "unittest", "tests/test_metadata.py"]

