import appdaemon.plugins.hass.hassapi as hass
import globals
import time
import datetime
import random
from datetime import timedelta

#
# Co2 report.
# 
# Args:
# entity - group of entities to send state report
# notify - notify entity to send message
# 
# Release Notes
#
# Version 1.0:
#   Initial Version

class AirQuality(hass.Hass):
  volume = 0.7
  co2_max_level = 1000
  def initialize(self):
    if 'alice' not in self.args or 'co2_sensor' not in self.args or 'ha_panel' not in self.args:
      self.error("Please provide alice, co2_sensor, ha_panel in config!")
      return

    self.timer = self.run_every(self.timer_tick, self.datetime()+timedelta(seconds=10), 1*60*60)

  def timer_tick(self, args) -> None:
    if 'constraint' in self.args and not self.constrain_input_boolean(self.args['constraint']):
      return
    home_state = self.get_state(self.args['ha_panel'])
    co2_value = int(float(self.get_state(self.args['co2_sensor'])))
    if home_state == "disarmed" and self.time_is_between(self.datetime(), '08:00:00', '23:59:59'):
      self.log('co2 level: {}'.format(co2_value))
      if co2_value > self.co2_max_level:
        self.warn_air_quality(co2_value)

  def warn_air_quality(self, co2_value):
    commands=[
      "Уровень ЦО2 достиг отметки {}... Пожалуйста, откройте окно.".format(co2_value),
      "Мне кажется у нас душно... Давайте откроем окно?",
      "ЦО2 растёт не по дням, а по часам... Уже {}... Давайте проветрим?".format(co2_value),
      "Кажется, я давно не была на улице... Давайте откроем окно и сделаем вид что гуляем?",
      "Пора открыть окошко, ЦО2 уже {}.".format(co2_value)
    ]
    random.shuffle(commands)
    self.say(commands[0])

  def command(self, command):
    self.call_service('yandex_station/send_command', command='sendText', text=command)

  def say(self, command):
    volume = self.get_state(self.args['alice'], 'volume_level')
    state = self.get_state(self.args['alice'])
    self.log('state: {}'.format(state))

    if state == "playing":
      self.call_service('media_player/media_pause', entity_id=self.args['alice'])

    self.call_service('media_player/volume_set', entity_id=self.args['alice'], volume_level=self.volume)    
    self.log('command = {}'.format(command))
    self.call_service('media_player/play_media', entity_id=self.args['alice'], media_content_type='text', media_content_id=command)
    self.run_in(self.run_in_volume, 10, volume=volume, state=state)

  def run_in_volume(self, kwargs):
    if 'volume' not in kwargs or 'state' not in kwargs:
      return
    volume = kwargs['volume']
    state = kwargs['state']
    self.log('setting volume back to {}'.format(volume))
    self.call_service('media_player/volume_set', entity_id=self.args['alice'], volume_level=volume)
    if state == "playing":
      self.log('resuming')
      # self.call_service('media_player/media_play', entity_id=self.args['alice'])

  def time_is_between(
          hass, target_dt: datetime, start_time: str,
          end_time: str) -> bool:
      """Generalization of AppDaemon's now_is_between method."""
      start_time_dt = hass.parse_time(start_time)  # type: datetime
      end_time_dt = hass.parse_time(end_time)  # type: datetime
      start_dt = target_dt.replace(
          hour=start_time_dt.hour,
          minute=start_time_dt.minute,
          second=start_time_dt.second)
      end_dt = target_dt.replace(
          hour=end_time_dt.hour,
          minute=end_time_dt.minute,
          second=end_time_dt.second)

      if end_dt < start_dt:
          # Spans midnight
          if target_dt < start_dt and target_dt < end_dt:
              target_dt = target_dt + timedelta(days=1)
          end_dt = end_dt + timedelta(days=1)
      return start_dt <= target_dt <= end_dt