FROM ubuntu:20.04
RUN apt-get update \
    && DEBIAN_FRONTEND=noninteractive TZ=Etc/UTC apt-get install tesseract-ocr -y && apt install tesseract-ocr-heb -y && apt install tesseract-ocr-all -y && apt install imagemagick -y\
    python3 \
    #python-setuptools \
    python3-pip
    #&& apt-get clean \
    #&& apt-get autoremove
ENV REFRESHED_AT 2014-07-01-5-50
ADD . /flask-deploy
WORKDIR /flask-deploy
RUN pip install -r requirements.txt
EXPOSE 8081
CMD gunicorn app:app --workers 2 --bind 0.0.0.0:8081 --timeout 800