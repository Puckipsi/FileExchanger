import socket



def get_domain_from_url(url: str) -> str:
    domain = url.split("//")[1].split("/")[0]
    return domain


def get_ip_from_domain(domain: str) -> str:
    ip_address = socket.gethostbyname(domain)
    return ip_address
