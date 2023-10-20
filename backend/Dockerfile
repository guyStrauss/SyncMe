FROM python:3.10.0-alpine AS base
LABEL authors="guy_strauss"
COPY backend /backend
COPY protos /backend/protos
COPY requirements.txt /backend/requirements.txt
WORKDIR /backend
RUN python3.10 -m pip install -r requirements.txt


FROM base AS prod
CMD ["python3.10", "file_sync_servicer.py"]

FROM base AS tests
CMD ["python3.10", "-m", "unittest", "discover", "-s", "tests"]



