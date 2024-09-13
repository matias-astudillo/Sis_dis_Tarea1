FROM python:3.9-slim
WORKDIR /app
RUN apt-get update && apt-get install -y dnsutils
RUN pip install grpcio==1.66.1
RUN pip install protobuf==5.27.2
COPY server.py .
COPY dns_pb2.py dns_pb2_grpc.py .
CMD ["python", "server.py"]