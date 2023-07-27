from pymisp import ExpandedPyMISP
from pycti import OpenCTIApiClient
from datetime import datetime, timedelta

def run_revoke_decayed_indicators():
    misp_url = "http://10.0.0.138"
    misp_key = "6DhrMkKEZjynpX0P8Z4o58YGxrYsiwFKEPtiPRH7"
    misp = ExpandedPyMISP(url=misp_url, key=misp_key, ssl=False)

    print("Running Revoking Script...")
    opencti_url = "http://10.0.0.138:8080"
    opencti_api = "1d2f63af-6fcc-4757-95fa-9c525a5375d2"
    opencti_client = OpenCTIApiClient(opencti_url, opencti_api)
    timestamp = datetime.now() - timedelta(30)
    
    decayed_iocs = misp.search(
        "attributes", 
        decayed=True, 
        include_decay_score=True, 
        timestamp=timestamp,
        tags=['!opencti_revoked'],
        type_attribute=['md5', 'sha1', 'sha256', 'domain', 'hostname', 'url', 'ip-dst', 'ip-src']
        )

    for decayed_ioc in decayed_iocs['Attribute']:
        decayed_ioc_val = decayed_ioc['value']
        opencti_indicator = opencti_client.indicator.read(filters=[{"key": "name", "values": [decayed_ioc_val]}])

        try:
            opencti_client.stix_domain_object.update_field(id=opencti_indicator['id'], input={"key": "revoked", "value": "true"})
            misp.tag(decayed_ioc, "opencti_revoked")
            print("Revoked " + decayed_ioc_val)
        except Exception as e:
            print("Revoke error on " + decayed_ioc_val)

    # [MISP] Get all indicators added with no opencti_revoked label and update score in opencti
    misp_not_revoked = misp.search(
        "attributes",
        type_attribute=['md5', 'sha1', 'sha256', 'domain', 'hostname', 'url', 'ip-dst', 'ip-src'],
        exclude_decayed=True,
        include_decay_score=True, 
        tags=['!opencti_revoked']
        )

    for attribute in misp_not_revoked['Attribute']:
        attribute_val = attribute['value']            
        opencti_indicator = opencti_client.indicator.read(filters=[{"key": "name", "values": [attribute_val]}])
        try:
            opencti_client.stix_domain_object.update_field(id=opencti_indicator['id'], input={"key": "x-opencti-score", "value": round(attribute['decay_score'][0]['score'])}) 
            print("Decayed " + attribute_val)
        except:
            print("Decay errored on " + attribute_val)

run_revoke_decayed_indicators()
