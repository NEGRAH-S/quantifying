# Standard library
import os
import sys
import traceback

# Third-Party Libary
import requests
# from requests.packages.urllib3.util.retry import Retry

def fetch_data (license_type, session):
    url = (
        r"https://commons.wikimedia.org/w/api.php?"
        r"action=query&prop=categoryinfo&format=json&titles="
        f"Category:{license_type}"
    )

    with session.get(url) as response:
        response.raise_for_status()
        search_result = response.json()
        print(search_result)

def main():
    session = requests.Session()
    license = 'cc-by'
    
    fetch_data(license, session)
    print('Complete')


if __name__ == "__main__":
    try:
        main()
    except SystemExit as e:
        sys.exit(e.code)
    except KeyboardInterrupt:
        print("INFO (130) Halted via KeyboardInterrupt.", file=sys.stderr)
        sys.exit(130)
    except Exception:
        print("ERROR (1) Unhandled exception:", file=sys.stderr)
        print(traceback.print_exc(), file=sys.stderr)
        sys.exit(1)

#     # Requests configurations
#     max_retries = Retry(
#         # try again after 5, 10, 20, 40, 80 seconds
#         # for specified HTTP status codes
#         total=5,
#         backoff_factor=10,
#         status_forcelist=[403, 408, 429, 500, 502, 503, 504],
#     )
#     session = requests.Session()
#     session.mount("https://", HTTPAdapter(max_retries=max_retries))