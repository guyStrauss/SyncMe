FROM mongo:latest
LABEL authors="guy_strausss"
RUN apt-get -y update
RUN apt-get install -y software-properties-common
RUN add-apt-repository -y ppa:deadsnakes/ppa
RUN apt-get install -y python3.10
RUN apt-get install -y python3-pip
COPY backend /backend
COPY protos /backend/protos
COPY requirements.txt /backend/requirements.txt
WORKDIR /backend
RUN python3.10 -m pip install -r requirements.txt
EXPOSE 50051
CMD ["python3.10", "file_sync_servicer.py"]
