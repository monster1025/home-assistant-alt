import appdaemon.plugins.hass.hassapi as hass

#
# Listen for Alarm panel state change and fire an events ('away_mode' and 'return_home_mode')
#
# Args:
# ha_panel - alarm control panel entity.
# Release Notes
#
# Version 1.0:
#   Initial Version

class PersonPresence(hass.Hass):
  def initialize(self):
    if "ha_panel" not in self.args:
      self.error("Please provide ha_panel in config!")
      return
    persons = self.get_state('person')
    for person in persons:
        self.listen_state(self.person_state_change, person)
    self.person_state_change(None, None, None, None, None)
    
  def person_state_change(self, entity, attribute, old, new, kwargs):
    ha_panel_state = self.get_state(self.args['ha_panel'])
    self.log('noone_home: {}, anyone_home: {}, panel_state: {}'.format(self.person_noone_home(), self.person_anyone_home(), ha_panel_state))

    if self.person_noone_home():
        self.log('Nobody home. Checking for panel is need to be switched.')
        if ha_panel_state != 'armed_away':
            self.log('armed_away')
            # self.call_service("alarm_control_panel/alarm_arm_away", entity_id = self.args['ha_panel'])
        return
    
    if self.person_anyone_home():
        self.log('Somebody home. Checking for panel is need to be switched.')
        if ha_panel_state != 'disarmed':
            # self.call_service("alarm_control_panel/alarm_disarm", entity_id = self.args['ha_panel'])
            self.log('disarmed')
        return
    self.log('Unknown state???')

  def person_noone_home(self):
    persons = self.get_state('person')
    for entity_id in persons.keys():
      if persons[entity_id]["state"] == "home":
        return False
    return True

  def person_anyone_home(self):
    persons = self.get_state('person')
    for entity_id in persons.keys():
      if persons[entity_id]["state"] == "home":
        return True
    return False