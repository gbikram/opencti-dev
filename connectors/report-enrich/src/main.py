import os
import sys
import time

import yaml
from pycti import OpenCTIConnectorHelper, get_config_variable


class TemplateConnector:
    def __init__(self):
        # Instantiate the connector helper from config
        config_file_path = os.path.dirname(os.path.abspath(__file__)) + "/config.yml"
        config = (
            yaml.load(open(config_file_path), Loader=yaml.FullLoader)
            if os.path.isfile(config_file_path)
            else {}
        )
        self.helper = OpenCTIConnectorHelper(config)
    ####
    # TODO add your code according to your connector type
    # For details: see
    # https://luatix.notion.site/luatix/Connector-Development-06b2690697404b5ebc6e3556a1385940
    ####
    def _process_message(self, data):
        print(data)

    def run(self):
        self.helper.listen(self._process_message)

if __name__ == "__main__":
    try:
        connector = TemplateConnector()
        connector.run()
    except Exception as e:
        print(e)
        time.sleep(10)
        sys.exit(0)
