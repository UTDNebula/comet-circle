FROM python:3.9.1

RUN pip install --upgrade pip

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r  requirements.txt 

# Change to follow GCP Cloud Run specification
ENV PORT=

# retrivied from https://discuss.streamlit.io/t/has-anyone-deployed-to-google-cloud-platform/931/21
RUN find /usr/local/lib/python3.9/site-packages/streamlit -type f \( -iname \*.py -o -iname \*.js \) -print0 | xargs -0 sed -i 's/healthz/health-check/g'

COPY main.py .
COPY data.py .
COPY Event.py . 
COPY heatmap_utils.py .

CMD streamlit run main.py --server.port=${PORT} --browser.serverAddress="0.0.0.0" --server.enableCORS False --server.enableXsrfProtection False