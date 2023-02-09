#!/usr/bin/env python
"""
This file is dedicated to obtain a .csv record report for Open Education Resources Commons data.
"""

import requests
import xml.etree.ElementTree as ET

ACCESS_TOKEN = "24edf58088875347463ba7fc13f5ffd25c1b5d72"
ENDPOINT = "https://www.oercommons.org/api/search"
BASE_URL = ENDPOINT + "?token=" + ACCESS_TOKEN

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
        f.write(response.text)

def main():
    test_access()

if __name__ == "__main__":
    main()
