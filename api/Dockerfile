FROM python:3.9-slim
WORKDIR /app
RUN pip install Flask==2.0.3
RUN pip install Werkzeug==2.0.3
RUN pip install redis==4.3.0
RUN pip install --upgrade grpcio
RUN pip install protobuf==5.27.2

COPY app.py .
COPY grpc_client.py .
COPY dns_pb2.py dns_pb2_grpc.py .
CMD ["python", "app.py"]

