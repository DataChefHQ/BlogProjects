FROM python

COPY requirements.txt requirements.txt
RUN pip install --no-cache -r requirements.txt

COPY model.py /usr/bin/model.py
COPY train.py /usr/bin/train
COPY serve.py /usr/bin/serve

RUN chmod 755 /usr/bin/train
RUN chmod 755 /usr/bin/serve

EXPOSE 8080