import appdaemon.plugins.hass.hassapi as hass

#
# This app will use motion sensors to turn on and off control_entity for 'timeout' time.
# It work with xiaomi motion sensors.
# main algorithm: when sensor turns on - turn on the light; when sensor is off - set timer for 'timeout'; 
# if sensor goes on - turn off the timer; when timer was hit - turn off the light.
#
# Args:
#
# sensor = motion sensor to use (will work with other sensor types too)
# timeout = timeout after sensor will turned off (keep in mind that xiaomi motion sensor has own timeout!)
# control_entity = entity, that will be controlled (example: group of light bulbs)
# constraint = you can define constraint (input_boolean), that will turn on and off this app.
#
# Release Notes
#
# Version 1.0:
#   Initial Version

class LightControlBath(hass.Hass):
  timer = None
  door_state_changed = None
  def initialize(self):
    if "sensor" not in self.args or 'door_sensor' not in self.args or "timeout" not in self.args or "control_entity" not in self.args:
      self.error("Please provide sensor, door_sensor, control_entity and timeout in config!")
      return
    self.listen_state(self.sensor_trigger, self.args['sensor'])
    self.listen_state(self.door_sensor_trigger, self.args['door_sensor'])

  def sensor_trigger(self, entity, attribute, old, new, kwargs):
    #sensor is off
    if new == 'off' and old == 'on':
      self.log('door_state_changed:{}'.format(self.door_state_changed))
      if self.door_state_changed == False:
        return
      self.log('Sensor is off - running timer for {}s.'.format(self.args['timeout']))
      self.run_timer()
    #sensor is on

    if new == 'on' and old == 'off':
      #turnin on control entity and wait while sensor will be off, than run timer.
      self.control_entity_on()
      self.stop_timer()
      door_state = self.get_state(self.args['door_sensor'])
      if door_state == "off":
        self.door_state_changed = False
      else :
        self.door_state_changed = None


  def door_sensor_trigger(self, entity, attribute, old, new, kwargs):
    #door is open
    sensor_state = self.get_state(self.args['sensor'])
    if new == 'on' and old == 'off' and sensor_state == 'off':
      self.log('door is opened now, runnig the timer')
      if self.timer == None:
        self.run_timer()
    if self.door_state_changed == False:
      self.door_state_changed = True
      self.log('door_state_changed:{}'.format(self.door_state_changed))

############ TIMER ########################  
  def control_entity_on(self):
    #if 'constraint' is off - we dont need to do anything
    if 'constraint' in self.args and not self.constrain_input_boolean(self.args['constraint']):
      return
    if self.get_state(self.args['control_entity']) == 'off':
      self.turn_on(self.args['control_entity'])
      self.log("Light on.")

  def control_entity_off(self, kwargs):
    #if 'constraint' is off - we dont need to do anything
    if 'constraint' in self.args and not self.constrain_input_boolean(self.args['constraint']):
      return
    if self.door_state_changed == False:
      self.log('Motion is detected inside and door is still closed - dont turn off the light')
      return
    if self.get_state(self.args['control_entity']) == 'on':
      self.turn_off(self.args['control_entity'])
      self.log("Light off.")
    self.stop_timer()

  def run_timer(self):
    if self.timer != None:
      self.stop_timer()
    self.timer = self.run_in(self.control_entity_off, self.args['timeout'])

  def stop_timer(self):
    if (self.timer == None):
      return
    self.log('stopping timer.')
    self.cancel_timer(self.timer)
    self.timer = None