FROM python:3.9-slim
WORKDIR /app
RUN pip install requests
COPY simulator.py .
COPY data_SD.csv .
CMD ["python", "simulator.py"]