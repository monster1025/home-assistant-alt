import appdaemon.plugins.hass.hassapi as hass
# from automation import Automation  # type: ignore

"""
Monitor events and output changes to the verbose_log. Nice for debugging purposes.
Arguments:
 - events: List of events to monitor
"""
class Monitor(hass.Hass):
    def initialize(self) -> None:
        # super().initialize()
        self.listen_event_handle_list = []

        events = self.args['events']

        if events != None:
            for event in self.split_device_list(self.args["events"]):
                self.log('watching event "{}" for state changes'.format(event))
                self.listen_event_handle_list.append(self.listen_event(self.changed, event))
        if len(self.listen_event_handle_list) == 0:
            self.log('watching all events for state changes')
            self.listen_event_handle_list.append(self.listen_event(self.changed))

    def changed(self, event_name, data, kwargs):
        self.log(event_name + ': ' + str(data))

    def terminate(self):
        for listen_event_handle in self.listen_event_handle_list:
            self.cancel_listen_event(listen_event_handle)
            