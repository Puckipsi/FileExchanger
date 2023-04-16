import socket
from ipaddress import ip_address
from typing import Union
import requests



def is_valid_url(url: str) -> dict[str, Union[bool, str]]:
    try:
        response = requests.head(url)
        response.raise_for_status()
        return {'valid': True, "message": "URL is valid and exists"}
    except (requests.exceptions.MissingSchema, requests.exceptions.InvalidURL):
        return {'valid': False, "message": "URL Invalid"}
    except requests.exceptions.HTTPError:
        return {'valid': False, "message": "URL exists but returned an error status code"}
    except requests.exceptions.ConnectionError:
        return {'valid': False, "message": "Could not connect to the URL"}

    
def is_valid_ip_address(ip: str) -> bool:
    try:
        ip_address(ip)
        return True
    except ValueError:
        return False


def get_domain_from_url(url: str) -> str:
    domain = url.split("//")[1].split("/")[0]
    return domain


def get_ip_from_domain(domain: str) -> str:
    ip_address = socket.gethostbyname(domain)
    return ip_address
