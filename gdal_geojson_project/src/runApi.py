import requests
from typing import Optional

config = {}
config.GIS_TOKEN_URL = "https://gis.israntique.org.il/portal/sharing/rest/generateToken"  # Replace with actual URL
config.GIS_USERNAME = "gisportal@IAA"  # Replace with actual username
config.GIS_PASSWORD = "Gpi$$8"  # Replace with actual password
config.GIS_REFERER_URL = "https://gis.israntique.org.il/portal"  # Replace with actual referer URL

def get_token() -> Optional[str]:
    """Function to get GIS token."""
    url = config.GIS_TOKEN_URL

    payload = {
        'username': config.GIS_USERNAME,
        'password': config.GIS_PASSWORD,
        'client': 'referer',
        'expiration': '24',
        'f': 'json',
        'referer': config.GIS_REFERER_URL
    }

    headers = {}
    files = []

    try:
        response = requests.post(url, headers=headers, data=payload, files=files)
        print(response.text)  # optional for debug
        return response.json().get('token')
    except Exception as e:
        print(f"Error while getting token: {e}")
        return None  
    
if __name__ == "__main__":
    token = get_token()
    if token:
        print(f"Token received: {token}")
    else:
        print("Failed to retrieve token.")
    