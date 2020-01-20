import appdaemon.plugins.hass.hassapi as hass
import globals
# from automation import Automation  # type: ignore

"""
Monitor events and output changes to the verbose_log. Nice for debugging purposes.
Arguments:
 - events: List of events to monitor
"""
class Test(hass.Hass):
    def initialize(self) -> None:
        if self.check_constain():
            return
        self.log('Script works')

    def check_constain(self, param_name='constrain'):
      self.log('checking constaint: {}'.format(param_name))
      if param_name not in self.args:
          self.log('script is not constrained')
          return True;
      constain_name = self.args[param_name]
      constain_state = self.get_state(constain_name)
      if constain_state == None:
        self.log('Constraint {} not found in hass. Creating new one.'.format(constain_name))
        attributes = {}
        attributes['description'] = 'Created and updated from appdaemon ({})'.format(__name__)
        self.set_state(constain_name, state = 'on', attributes = attributes)
      if not self.constrain_input_boolean(constain_name):
        self.log('Script {} is off.'.format(__name__))
        return False
      self.log('state: {}'.format(constain_state))