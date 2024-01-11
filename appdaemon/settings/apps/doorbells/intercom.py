import appdaemon.plugins.hass.hassapi as hass
import os

#
# App to send notification when doorbell is ringing
#
# Args:
#
# notify = notification platform to send notifications to
#
# None
#
# Release Notes
#
# Version 1.0:
#   Initial Version

class Intercom(hass.Hass):
  is_blocked = False
  timer = None

  def initialize(self):
    if "notify" not in self.args or "sensor" not in self.args:
      self.error("Please provide notify, sensor in config!")
      return

    self.listen_state(self.sensor_trigger, self.args['sensor'])

  def sensor_trigger(self, entity, attribute, old, new, kwargs):
    if old == "" or old == "unknown":
      return

    if new == "ring" and self.is_blocked == False:
      self.log("intercom call")
      self.log("old: {}, new: {}".format(old, new))
      self.say("Звонок в домофон!!!")
      self.notify("Звонок в домофон!!! ({}, {})".format(old, new), name = self.args['notify'])
      self.is_blocked = True
      self.run_timer()

  def run_timer(self):
    if self.timer != None:
      self.stop_timer()
    self.timer = self.run_in(self.unblock_msg, self.args['timeout'])
  
  def stop_timer(self):
    if (self.timer == None):
      return
    self.log('stopping timer.')
    self.cancel_timer(self.timer)
    self.timer = None


  def unblock_msg(self, kwargs):
    self.log('stopping timer')
    self.is_blocked = False

  def say(self, command):
    self.log('command = {}'.format(command))
    self.call_service('media_player/play_media', entity_id=self.args['alice'], media_content_type='text', media_content_id=command)