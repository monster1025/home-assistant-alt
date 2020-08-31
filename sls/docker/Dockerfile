FROM python:latest

ADD ./backup.py /backup.py
ADD ./run.sh /run.sh
ADD ./requirements.txt /requirements.txt
RUN chmod +x /run.sh && pip3 install -r /requirements.txt

CMD [ "bash", "/run.sh" ]