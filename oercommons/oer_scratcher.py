#!/usr/bin/env python
"""
This file is dedicated to obtain a .csv record report for Open Education Resources Commons data.
"""

import csv
import xml.etree.ElementTree as ET
import re
import requests

import query_secrets

ENDPOINT = "https://www.oercommons.org/api/search"
BASE_URL = f"{ENDPOINT}?token={query_secrets.ACCESS_TOKEN}" 

def get_license_list():
    """Returns list of licenses to query."""
    return [
        "cc-nc-sa",
        "cc-by",
        "cc-by-sa",
        "cc-by-nd",
        "cc-by-nc",
        "cc-by-nc-sa",
        "cc-by-nc-nd"
    ]

def get_license_total_count(license):
    """Returns total items for a license."""
    response = requests.get(f'{BASE_URL}&f.license={license}&batch_size=0')
    root = ET.fromstring(re.sub(r"&\w*;", "", response.text))
    return root.attrib['total-items']


def batch_retrieve(license, batch_start, writer):
    """Returns ET object with the next 10 results."""
    response = requests.get(f'{BASE_URL}&f.license={license}&batch_size=50&batch_start={batch_start}')
    root = ET.fromstring(re.sub(r"&\w*;", "", response.text))
    # TODO: parse and write to file


def record_license_data(license, writer):
    """Retrieve all data for a license."""
    total = get_license_total_count(license)
    current_index = 0
    # TODO: don't run yet, only test smaller batches
    # while current_index < total:
    # TODO: for testing purposes
    while current_index < 100:
        batch_retrieve(license, current_index, writer)
        current_index += 50


def record_all_licenses():
    """Records the data of all license types."""
    license_list = get_license_list()
    with open('oer.csv', 'w', newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["license", "education_level", "subject_area",
            "material_type", "media_format", "languages", "primary_user", 
            "educational_use", "modification_date"])
        # TODO: don't run yet, only test smaller batches
        # for license_type in license_list:
        #     record_license_data(license_type, writer)
        # TODO: for testing purposes
        record_license_data(license_list[0], writer)


def test_access():
    """Tests endpoint by filtering under cc-by license."""
    response = requests.get(f'{BASE_URL}&f.license=cc-by&batch_size=50') 
    print(response.status_code)
    with open('data.xml', 'w') as f:
        print(type(response.text))
        f.write(re.sub(r"&\w*;", "", response.text))
    # root = ET.fromstring(re.sub(r"&\w*;", "", response.text))
    # license_total = root.find('oersearchresults').attrib['total-items']
    # print(license_total)


def test_xml_parse():
    """Tests getting elements from XML."""
    tree = ET.parse('data.xml')
    root = tree.getroot()
    # Gets license total
    for i in root.iter('result'):
        print(i.attrib['total-items'])


def main():
    test_access()
    # test_xml_parse()
    # print(get_license_total_count('cc-by'))
    # record_all_licenses()

if __name__ == "__main__":
    main()
