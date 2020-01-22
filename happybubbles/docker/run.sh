#!/bin/sh

# modify the mqtt username, password, and host_path for your setup, host path includes the host and port 

while true
do
	if [ "$MQTT_USERNAME" != "" ] && [ "$MQTT_PASSWORD" != "" ] && [ "$MQTT_HOST_PORT" != "" ];
	then
			./app -http_host_path=0.0.0.0:5555 -mqtt_username=$MQTT_USERNAME -mqtt_password=$MQTT_PASSWORD -mqtt_host=$MQTT_HOST_PORT
	else
		echo "Please provide MQTT_USERNAME, MQTT_PASSWORD, MQTT_HOST_PORT"
	fi
	sleep 5
done