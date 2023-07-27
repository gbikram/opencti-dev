import os
import time
import yaml
from pycti import OpenCTIConnectorHelper, get_config_variable
from typing import Dict

class BulkCsvImporter:
    def __init__(self):
        # Instantiate the connector helper from config
        config_file_path = os.path.dirname(os.path.abspath(__file__)) + "/../config.yml"
        config = (
            yaml.load(open(config_file_path), Loader=yaml.FullLoader)
            if os.path.isfile(config_file_path)
            else {}
        )
        self.helper = OpenCTIConnectorHelper(config)
        self.cve_interval = get_config_variable(
            "TEMPLATE_ATTRIBUTE", ["template", "attribute"], config, True
        )


    def _process_message(self, data: Dict) -> str:
        self.helper.log_info("Processing new message")
        print(data)			

        # Start the main loop
    def start(self) -> None:
        self.helper.listen(self._process_message)