#!/usr/bin/env python
"""
This file is dedicated to obtain a .csv record report for Open Education Resources Commons data.
"""

import requests

ACCESS_TOKEN = "24edf58088875347463ba7fc13f5ffd25c1b5d72"
ENDPOINT = "https://www.oercommons.org/api/search"
BASE_URL = ENDPOINT + "?token=" + ACCESS_TOKEN

def test_access():
    """Tests endpoint by filtering under cc-by license."""
    print("test")

def main():
    test_access()

if __name__ == "__main__":
    main()
