#!/bin/sh
while true
do
  echo "token=$TOKEN" > /yandex-ddns.toml
  echo "domain=$DOMAIN" >> /yandex-ddns.toml
  echo "subdomain=$SUBDOMAIN" >> /yandex-ddns.toml
  echo "ttl=$TTL" >> /yandex-ddns.toml
  chmod 600 /yandex-ddns.toml
  #cat /yandex-ddns.toml
  ./app
  sleep 5m
done
