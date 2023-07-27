import os
import time

import yaml
from pycti import OpenCTIConnectorHelper, get_config_variable
from bulkcsvimporter import BulkCsvImporter

if __name__ == "__main__":
    try:
        template_connector = BulkCsvImporter()
        template_connector.start()
    except Exception as e:
        print(e)
        time.sleep(10)
        exit(0)