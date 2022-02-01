FROM python:3.9.1

RUN pip install --upgrade pip

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r  requirements.txt 

# Change to follow GCP Cloud Run specification
ENV PORT=


COPY main.py .
COPY data.py .
COPY Event.py . 
COPY heatmap_utils.py .

CMD streamlit run main.py --server.port=${PORT} --browser.serverAddress="0.0.0.0"