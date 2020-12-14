import appdaemon.plugins.hass.hassapi as hass
import datetime

#
# App to send email report for devices running low on battery
#
# Args:
#
# threshold = value below which battery levels are reported and email is sent
# always_send = set to 1 to override threshold and force send
#
# None
#
# Release Notes
#
# Version 1.0:
#   Initial Version

class Flower(hass.Hass):

  def initialize(self):
    #self.check_batteries({"force": 1})
    time = datetime.time(21, 0, 0)
    self.run_daily(self.check_flowers, time)
    # self.log('---------------------')
    # self.check_flowers([])
    
  def check_flowers(self, kwargs):
    if 'constraint' in self.args and not self.constrain_input_boolean(self.args['constraint']):
      return

    devices = self.get_state()
    values = {}
    low = []
    for deviceName in devices:
      device = devices[deviceName]
      if device == None:
        continue
      if '_soil_moisture' not in deviceName or 'avocado' not in deviceName:
        continue
      # self.log('found: {}'.format(device))

      moisture = int(device['state'])
      if moisture != None:
        if moisture < self.args["threshold"] and moisture != 0:
          low.append(deviceName)
        values[deviceName] = moisture

    message=""
    if low:
      message += "Пора полить цветочки: (< {}) \n".format(self.args["threshold"])
      for device in low:
        message += "{}: {}%\n".format(self.friendly_name(device), values[device])
      message += "\n\n"
          
    if low or ("always_send" in self.args and self.args["always_send"] == 1) or ("force" in kwargs and kwargs["force"] == 1):
      if message != "":
        self.notify(message, name = "telegram")
        self.call_service('media_player/play_media', entity_id=self.args['alice'], media_content_type='text', media_content_id="Пора полить цветочки.")
