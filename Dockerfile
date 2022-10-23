FROM python:3.9-slim

RUN echo PORT $PORT

EXPOSE 1080

WORKDIR /app

COPY . /app

RUN apt-get update && apt-get install -y \
    build-essential \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*

RUN git clone https://github.com/streamlit/streamlit-example.git 

RUN pip3 install -r requirements.txt

# RUN sh setup.sh

# RUN streamlit run streamlit_app.py 

ENTRYPOINT ["streamlit", "run", "streamlit_app.py" "--server.port", "`$PORT`", "--server.address", "0.0.0.0"]
