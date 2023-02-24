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
    print("Success")
    return root.attrib['total-items']


def get_all_license_count(api_usage):
    """Saves total license count to disk."""
    license_count = []
    if api_usage:
        license_lst = get_license_list() 
        for lcs in license_lst:
            license_count.append(get_license_total_count(lcs))
        with open("license_counts.csv", 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(license_lst)
            writer.writerow(license_count)
    else:
        with open("license_counts.csv", "r") as file:
            next(file)
            license_count = list(map(int, next(file).replace("\n", "").split(',')))
    return license_count


def batch_retrieve(license, batch_start, writer):
    """Returns ET object with the next 50 results."""
    response = requests.get(f'{BASE_URL}&f.license={license}&batch_size=50&batch_start={batch_start}')
    root = ET.fromstring(re.sub(r"&\w*;", "", response.text))

    for result in root:
        for attribute in result:
            # Modification Date
            if attribute.tag == 'modification_date':
                date = attribute.text
            # OER Summary Data
            elif attribute.tag == 'oersummary':
                temp = {
                    "Education Level": "",
                    "Subject Area": "",
                    "Material Type": "",
                    "Media Format": "",
                    "Languages": "",
                    "Primary User": "",
                    "Educational Use": ""
                }

            for item in attribute:
                if temp.get(item.attrib['title']) is not None:
                    temp[item.attrib['title']] = item.attrib['value']
            writer.writerow([license] + [date] + list(temp.values()))


def record_license_data(license, total, writer):
    """Retrieve all data for a license."""
    current_index = 0
    # TODO: for testing purposes
    while current_index < 100: # actual: while current_index < total
        batch_retrieve(license, current_index, writer)
        current_index += 50


def record_all_licenses():
    """Records the data of all license types."""
    license_list = get_license_list()
    license_count = get_all_license_count(False)
    with open('oer.csv', 'w', newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["license", "Education Level", "Subject Area",
            "Material Type", "Media Format", "Languages", "Primary User", 
            "Educational Use", "modification_date"])
        # TODO: don't run yet, only test smaller batches
        # for x in range(0, len[license_list]:
        #     record_license_data(license_type[x], license_count[x], writer)
        # TODO: for testing purposes
        record_license_data(license_list[0], license_count[0], writer)


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

    row_data = ['cc-by']
    for result in root:
        id = [result.attrib]
        for attribute in result:
            # Modification Date
            if (attribute.tag == 'modification_date'):
                date = [attribute.text]
            # OER Summary
            if (attribute.tag == 'oersummary'):
                temp = {
                    "Education Level": "",
                    "Subject Area": "",
                    "Material Type": "",
                    "Media Format": "",
                    "Languages": "",
                    "Primary User": "",
                    "Educational Use": ""
                }

                for item in attribute:
                    if temp.get(item.attrib['title']) is not None:
                        temp[item.attrib['title']] = item.attrib['value']
                
                print(id + row_data + date + list(temp.values()))


def main():
    # test_access()
    test_xml_parse()
    # print(get_license_total_count('cc-by'))
    # record_all_licenses()
    # print(get_all_license_count(False))

if __name__ == "__main__":
    main()
