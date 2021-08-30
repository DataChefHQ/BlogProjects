FROM python:3.7

RUN pip3 install --no-cache scikit-learn numpy pandas joblib sktime
RUN pip3 install --no-cache flask

COPY docker-training.py /usr/bin/train
COPY docker-serve.py /usr/bin/serve

RUN chmod 755 /usr/bin/train /usr/bin/serve

EXPOSE 8080
