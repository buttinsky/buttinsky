from modules.util import hpfeeds

from configobj import ConfigObj

from base_logger import BaseLogger


class HPFeedsLogger(BaseLogger):

    def __init__(self):
        self.buttinsky_config = ConfigObj("conf/buttinsky.cfg")
        if self.buttinsky_config["hpfeeds"]["enabled"] == "False":
            self.options = {'enabled': 'False'}
            return

        def on_error(payload):
            self.hpc.stop()

        def on_message(ident, chan, content):
            print content
        try:
            self.hpc = hpfeeds.new(self.buttinsky_config["hpfeeds"]["host"],
                                   int(self.buttinsky_config["hpfeeds"]["port"]),
                                   self.buttinsky_config["hpfeeds"]["ident"],
                                   self.buttinsky_config["hpfeeds"]["secret"])
            self.hpc.connect()
            self.options = {'enabled': 'True'}
        except KeyError:
            pass

    def insert(self, data):
        for chaninfo in self.buttinsky_config["hpfeeds"]["publish_channels"]:
            self.hpc.publish(chaninfo, data)
