# Standard library
import os
import sys
import traceback

# Third-Party Libary
import requests
from requests.packages.urllib3.util.retry import Retry

def get_imageinfo(image_name):
    url = (
        r"https://commons.wikimedia.org/w/api.php?"
        r"action=query&titles="
        f"{image_name}&prop=imageinfo&format=json"
    )

    return url



def get_categorymembers (license_type, session):
    license_type= "CC-BY-3.0,2.5,2.0,1.0"
    url = (
        # r"https://commons.wikimedia.org/w/api.php?"
        # r"action=query&prop=categoryinfo&titles="
        # f"Category:{license}&format=json"
        
        r"https://commons.wikimedia.org/w/api.php?"
        r"action=query&list=categorymembers"
        r"&cmlimit=500&cmtype=file&cmtitle="
        f"Category:{license_type}&format=json"
    )



    with session.get(url) as response:
        response.raise_for_status()
        search_result = response.json()

    category_members = []
    for member in search_result["query"]["categorymembers"]:
        category_members.append((member["pageid"], member["title"]))
    
    return category_members

def get_image_timestamp_list (image_list, session):
    year_dict = {}

    for member in image_list:
        image_url = get_imageinfo(member[1])
        with session.get(image_url) as response:
            response.raise_for_status()
            image_result = response.json()

        year = str(image_result["query"]["pages"][str(member[0])]["imageinfo"][0]["timestamp"])[0:4]
        if year in year_dict:
            year_dict[year] += 1 
        else:
            year_dict[year] = 1
    print(year_dict)    
    return year_dict
        

# def set_up_data_file():
#     """Writes the header row to file to contain WikiCommons Query data."""
#     header_title = "LICENSE TYPE,File Count,Page Count\n"
#     with open(DATA_WRITE_FILE, "w") as f:
#         f.write(header_title)
        


def main():
    # Requests configurations
    max_retries = Retry(
        # try again after 5, 10, 20, 40, 80 seconds
        # for specified HTTP status codes
        total=5,
        backoff_factor=10,
        status_forcelist=[403, 408, 429, 500, 502, 503, 504],
    )
    
    session = requests.Session()
    license_list = 'cc-by'
    # set_up_data_file()
    
    images = get_categorymembers(license_list, session)
    get_image_timestamp_list(images, session)

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