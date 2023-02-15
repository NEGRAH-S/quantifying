#!/usr/bin/env python
"""
This file is dedicated to obtain a .csv record report for Open Education Resources Commons data.
"""

import requests
import re
import xml.etree.ElementTree as ET

import query_secrets

ENDPOINT = "https://www.oercommons.org/api/search"
BASE_URL = f"{ENDPOINT}?token={query_secrets.ACCESS_TOKEN}" #change to f string

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
    response = requests.get(f'{BASE_URL}&f.license=cc-by&batch_size=10') # change to f string
    print(response.status_code)
    with open('data.xml', 'w') as f:
        print(type(response.text))
        f.write(re.sub(r"&\w*;", "", response.text))
    root = ET.fromstring(re.sub(r"&\w*;", "", response.text))
    license_total = root.find('oersearchresults').attrib['total-items']
    print(license_total)

def test_xml_parse():
    """Tests getting elements from XML."""
    tree = ET.parse('data.xml')
    root = tree.getroot()
    # Gets license total
    for i in root.iter('oersearchresults'):
        print(i.attrib['total-items'])


def main():
    # test_access()
    test_xml_parse()

if __name__ == "__main__":
    main()
