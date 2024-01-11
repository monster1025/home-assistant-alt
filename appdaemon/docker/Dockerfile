FROM python:latest

VOLUME /conf
VOLUME /certs
EXPOSE 5050

RUN apt-get update && apt-get install -y git

# Copy appdaemon into image
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

# Download and build appdaemon, 4.0.0b2
# --branch=4.0.0b1
RUN git clone --recurse-submodules https://github.com/home-assistant/appdaemon.git .
RUN pip3 install requests python-dateutil && pip install --upgrade pip .

# Start script
RUN chmod +x /usr/src/app/dockerStart.sh

RUN pip3 install \
      attrs==19.1.0 \
      #emp_mos_api==0.12 \
      packaging==16.8 \
      #python-Levenshtein==0.12.0 \
      voluptuous==0.11.5

ADD ./emp_mos_api /emp_mos_api

CMD [ "./dockerStart.sh" ]
