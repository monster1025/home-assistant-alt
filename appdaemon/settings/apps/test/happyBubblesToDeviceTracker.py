import appdaemon.plugins.hass.hassapi as hass
import appdaemon.plugins.mqtt.mqttapi as mqtt
import globals
import json
import random

"""
Monitor events and output changes to the verbose_log. Nice for debugging purposes.
Arguments:
 - events: List of events to monitor
"""

class HappyBubblesToDeviceTracker(mqtt.Mqtt):
    base_topic = "happy-bubbles/presence/ha"
    def initialize(self) -> None:
        self.log('Initialize HappyBubblesToDeviceTracker')
        self.mqtt_subscribe('{}/#'.format(self.base_topic), namespace='mqtt')
        self.listen_event(self.event_listener, 'MQTT_MESSAGE', namespace='mqtt')
    
    def event_listener(self, event_name, data, kwargs):
        topic = data.get('topic', '')
        if self.base_topic	not in topic:
        	return
        location = topic.replace('{}/'.format(self.base_topic), "")

        payload = json.loads(data['payload']) if data.get('payload') else {}
        # self.log('[{}] topic: {}, payload: {}'.format(event_name, topic, payload))
        id = payload.get('id', None)
        name = payload.get('name', None)
        distance = payload.get('distance', None)

        hb_topic="happy-bubbles/location/{}".format(id)
        self.mqtt_publish(hb_topic, location, qos = 0, retain = False, namespace='mqtt')
        
        self.log('Beacon {} ({}) moved to {} (distance: {}).'.format(name, id, location, distance))
