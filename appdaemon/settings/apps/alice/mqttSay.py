import appdaemon.plugins.hass.hassapi as hass
import appdaemon.plugins.mqtt.mqttapi as mqtt
import globals
import json
import random
import time
import datetime

class MqttSay(mqtt.Mqtt, hass.Hass):
    base_topic = "home/AliceBig/say"

    def initialize(self) -> None:
        self.log('Initialize Alice say plugin')

        self.base_topic = self.args.get('topic', self.base_topic)
        self.log('Listening for {}'.format(self.base_topic))

        self.mqtt_subscribe(self.base_topic, namespace='mqtt')
        self.listen_event(self.event_listener, 'MQTT_MESSAGE', namespace='mqtt')
    
    def event_listener(self, event_name, data, kwargs):
        if self.base_topic != data['topic']:
            return
        self.say(data['payload'])

    def command(self, command):
      self.call_service('yandex_station/send_command', command='sendText', text=command)

    def say(self, command):
      # self.call_service('media_player/volume_set', entity_id=self.args['alice'], volume_level=0.6)    
      self.call_service('media_player/play_media', entity_id=self.args['alice'], media_content_type='text', media_content_id=command)
