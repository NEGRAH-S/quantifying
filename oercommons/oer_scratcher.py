#!/usr/bin/env python
"""
This file is dedicated to obtain a .csv record report for Open Education Resources Commons data.
"""

import requests
import re
import xml.etree.ElementTree as ET

import query_secrets

ENDPOINT = "https://www.oercommons.org/api/search"
BASE_URL = ENDPOINT + "?token=" + query_secrets.ACCESS_TOKEN

def works_per_license():
    licenses = [
        "CC",
        "CC-BY",
        "CC-BY-NC",
        "CC-BY-NC-ND",
        "CC-BY-NC-SA",
        "CC-BY-ND",
        "CC-BY-SA",
        "CC-BY-ND" # no longer available?
    ]
    
    

def test_access():
    """Tests endpoint by filtering under cc-by license."""
    response = requests.get(BASE_URL + '&f.license=cc-by&batch_size=10')
    print(response.status_code)
    with open('data.xml', 'w') as f:
        print(type(response.text))
        f.write(re.sub("&\w*;", "", response.text))
    root = ET.fromstring(re.sub("&\w*;", "", response.text))
    license_total = root.iter('oersearchresults')
    print(license_total)


def main():
    test_access()

if __name__ == "__main__":
    main()
