import appdaemon.plugins.hass.hassapi as hass

"""
Monitor events and output changes to the verbose_log. Nice for debugging purposes.
Arguments:
 - events: List of events to monitor
"""
class Test(hass.Hass):
    notify = None

    def initialize(self) -> None:
      self.log('ok')
      self.notify = self.get_app('notify')
      # self.notify.notify_person('ok2', target='danil')
      