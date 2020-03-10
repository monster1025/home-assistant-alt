import appdaemon.plugins.hass.hassapi as hass
import globals

#
# Home and away report
# Send report about home state after presence_actions was done.
# 
# Args:
# entity - group of entities to send state report
# notify - notify entity to send message
# 
# Release Notes
#
# Version 1.0:
#   Initial Version

class PresenceAction(hass.Hass):
  report_delay = 15
  def initialize(self):
    if 'alice' not in self.args:
      self.error("Please provide alice in config!")
      return
    self.listen_event(self.away_mode, "away_mode")
    self.listen_event(self.return_home_mode, "return_home_mode")

  def away_mode(self, event_id, event_args, kwargs):
    if 'constraint' in self.args and not self.constrain_input_boolean(self.args['constraint']):
      return
    self.exec_command('стоп')

  def return_home_mode(self, event_id, event_args, kwargs):
    if 'constraint' in self.args and not self.constrain_input_boolean(self.args['constraint']):
      return
    self.exec_command('продолжить')

  def exec_command(self, command):
    self.call_service('media_player/play_media', entity_id=self.args['alice'], media_content_type='command', media_content_id=command)