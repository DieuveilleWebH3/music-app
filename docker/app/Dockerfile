#FROM continuumio/anaconda3
FROM python:3.7
#RUN apt-get install software-properties-common --fix-missing -y
#RUN add-apt-repository ppa:sandromani/gimagereader

RUN apt-get update && apt-get upgrade -y \
    && apt-get install -y \
        apt-transport-https \
        libpq-dev \
        build-essential \
        git \
        sudo \
        cmake zlib1g-dev libjpeg-dev xvfb xorg-dev libboost-all-dev libsdl2-dev swig ca-certificates \
        unzip zip nano\
        poppler-utils \
        pdftohtml \
        curl\
        tesseract-ocr \
        ghostscript\
        libtesseract-dev \
        python-dev libxml2-dev libxslt1-dev antiword\
        unoconv\
        ffmpeg libsm6 libxext6\
    && rm -rf /var/lib/apt/lists/*


# Installing the Tensorflow Object Detection API (https://gilberttanner.com/blog/installing-the-tensorflow-object-detection-api)
RUN git clone --depth 1 https://github.com/tensorflow/models.git

# Install object detection api dependencie
#RUN conda update -n base conda
#RUN conda install -y joblib         
#RUN conda install -y -c conda-forge tensorflow==1.15
RUN pip install Cython && \
    pip install contextlib2

# Get protoc 3.0.0, rather than the old version already in the container

RUN curl -k -OL "https://github.com/google/protobuf/releases/download/v3.0.0/protoc-3.0.0-linux-x86_64.zip" && \
    unzip protoc-3.0.0-linux-x86_64.zip -d proto3 && \
    mv proto3/bin/* /usr/local/bin && \
    mv proto3/include/* /usr/local/include && \
    rm -rf proto3 protoc-3.0.0-linux-x86_64.zip

# Run protoc on the object detection repo
RUN cd models/research && \
    protoc object_detection/protos/*.proto --python_out=.

# Set the PYTHONPATH to finish installing the API
ENV PYTHONPATH=$PYTHONPATH:/models/research/slim
ENV PYTHONPATH=$PYTHONPATH:/models/research

RUN apt-get update && apt-get -y -q install libreoffice libreoffice-writer


COPY ./requirements.txt /root/requirements.txt
RUN pip install --use-deprecated=legacy-resolver -r /root/requirements.txt


#RUN apt-get update && \
#    apt install default-jdk -y

#RUN python -m nltk.downloader punkt
# Entrypoint

CMD ['python', '/app/manage.py', 'runserver' , '0.0.0.0:8000']