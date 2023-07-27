from pycti import OpenCTIApiClient 
import stix2

indicator_value = "testindicator33.local"

opencti_api_client = OpenCTIApiClient("http://10.0.0.138:8080", "1d2f63af-6fcc-4757-95fa-9c525a5375d2")

stix_indicator = opencti_api_client.indicator.create(
    pattern=f"[domain:value = '{indicator_value}']",
    pattern_type="stix",
    allow_custom=True,
    name=indicator_value,
    object_marking_refs=[stix2.TLP_AMBER.get("id")],
    labels=["hygiene"], 
    x_opencti_main_observable_type="Domain-Name",
    x_opencti_create_observables=True,
    confidence=90,
    x_opencti_score=20
)

