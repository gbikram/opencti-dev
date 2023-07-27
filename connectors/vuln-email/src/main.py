import os
import sys
import time

import yaml
from pycti import OpenCTIConnectorHelper, get_config_variable

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

class VulnEmailConnector:
    def __init__(self):
        # Instantiate the connector helper from config
        config_file_path = os.path.dirname(os.path.abspath(__file__)) + "/config.yml"
        config = (
            yaml.load(open(config_file_path), Loader=yaml.FullLoader)
            if os.path.isfile(config_file_path)
            else {}
        )
        self.helper = OpenCTIConnectorHelper(config)
        self.cve_interval = get_config_variable(
            "TEMPLATE_ATTRIBUTE", ["template", "attribute"], config, True
        )
        self.email_pass = get_config_variable(
            "EMAIL_PASS", ["connector", "email_pass"], config
        )

    def prepare_msg_html(self, data):
        entity_id = data['entity_id']
        
        vuln_data = self.helper.api.vulnerability.read(id=entity_id)
        print(vuln_data) 
        # Message Container
        msg = MIMEMultipart('alternative')
        msg['subject'] = 'Vulnerability Alert'
        msg['From'] = 'octi_auto@octiadmin.local'
        msg['To'] = 'intel_pdl@testdomain.local'

        vuln_name = vuln_data['name']
        vuln_description = vuln_data['description']

        html = ""  
        with open('template.html', 'r') as template:
            html = template.read()
        
        html_gen = html.format(**locals())
        print(html_gen)

        with open('html_output.html', 'w') as html_output:
            html_output.write(html_gen)
        msg_body = MIMEText(html_gen, 'html')

        msg.attach(msg_body)
        
        return msg

    def send_email(self, msg):
        sender = "ghurabikram@gmail.com"
        rec = "gbikram.work@gmail.com"
        password = self.email_pass
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender, password)
        print("Logged in!")
        server.sendmail(sender, rec, msg.as_string())
        server.quit()
        print("sent!")        

    def _process_message(self, data):
        
        msg = self.prepare_msg_html(data)
        self.send_email(msg)

    def start(self):
        self.helper.listen(self._process_message)

if __name__ == "__main__":
    try:
        connector = VulnEmailConnector()
        connector.start()
        # connector.send_msg()
    except Exception as e:
        print(e)
        time.sleep(10)
        sys.exit(0)
