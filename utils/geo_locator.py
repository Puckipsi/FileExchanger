import geocoder
from utils.url import get_domain_from_url, get_ip_from_domain
from utils.config import Config


class GeoLocator:

    def __init__(self) -> None:
        self.config = Config()


    def get_hosts_ip_address(self) -> list:
        hosts = self.config.get_available_hosts()
        return [get_domain_from_url(host) for host in hosts]
    
    def get_host_url_by_ip(self, ip_address: str) -> str:
        hosts = self.config.get_available_hosts()
        url = [host for host in hosts if ip_address in host]
        return url[0]


    def get_domain_ip_adddress_from_url(self, url: str) -> str:
        domain = get_domain_from_url(url)
        domain_ip_adddress = get_ip_from_domain(domain)
        return domain_ip_adddress
    

    def get_location_by_ip(self, ip_address: str) -> geocoder.ipinfo:
        location = geocoder.ip(ip_address)
        return location
    

    def get_distance_between_hosts(self, target_host_location: list, host_location: list) -> float:
        distance = geocoder.distance(target_host_location, host_location)
        return distance
    

    def distance_between_hosts(self, target_url: str = '', hosts: list = []) -> dict:
        distances = {}
        target_host_ip = self.get_domain_ip_adddress_from_url(target_url)
        target_host_location = self.get_location_by_ip(target_host_ip).latlng
    
        for host in hosts:
            host_location = self.get_location_by_ip(host).latlng
            distance = self.get_distance_between_hosts(target_host_location, host_location)
            distances[host] = distance

        return distances

    def find_nearest_host(self, target_url: str) -> str:
        hosts = self.get_hosts_ip_address()
        distances = self.distance_between_hosts(target_url, hosts)
        nearest_host = min(distances, key=distances.get)
        host_url = self.get_host_url_by_ip(nearest_host)
        return host_url
