FROM ubuntu

RUN apt-get update && \
    apt-get install -y curl build-essential bluetooth bluez libbluetooth-dev libudev-dev libusb-1.0-0-dev git && \
    rm -rf /var/lib/apt/lists/*

RUN curl -sL https://deb.nodesource.com/setup_10.x | bash - && \
    apt-get install -y nodejs && \
    rm -rf /var/lib/apt/lists/*


WORKDIR /room-assistant

RUN git clone https://github.com/monster1025/room-assistant  .
ADD ./package.json package.json
RUN npm install --production && ln -s /data/options.json config/local.json

CMD [ "/usr/bin/npm", "start" ]
