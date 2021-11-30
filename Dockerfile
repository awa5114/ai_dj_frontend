FROM python:3.8.6-buster

COPY ai_dj /ai_dj
COPY app.py /app.py
COPY MANIFEST.in /MANIFEST.in
COPY pipeline.pkl /pipeline.pkl
COPY Procfile /Procfile
COPY setup.py /setup.py
COPY setup.sh /setup.sh
COPY requirements.txt /requirements.txt

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

RUN mkdir -p ~/.streamlit/

# RUN echo "\
# [general]\n\
# email = \"${HEROKU_EMAIL_ADDRESS}\"\n\
# " > ~/.streamlit/credentials.toml

# RUN echo "\
# [server]\n\
# headless = true\n\
# enableCORS = false\n\
# port = $PORT\n\
# " > ~/.streamlit/config.toml

RUN apt-get update -y && apt-get install -y --no-install-recommends build-essential gcc \
                                        libsndfile1  
                                        
EXPOSE 8501
ENTRYPOINT ["streamlit", "run"]

CMD ["app.py"]