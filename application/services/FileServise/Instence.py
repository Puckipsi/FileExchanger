from enum import Enum
from ec2_metadata import ec2_metadata
from dotenv import dotenv_values


config = dotenv_values('.env')
env_infrastruct = config['ENVIRONMENT_INFRASTRUCT']


class AWSRegion(Enum):
    eu = 'Europe'
    us = 'US'
    ap = 'Asia Pacific'
    ca = 'Canada'
    sa = 'South America'



class EC2Instance:

    InstanceId = ec2_metadata.instance_id if env_infrastruct == 'AWS' else ''
    InstanceLocationRegion = ec2_metadata.region if env_infrastruct == 'AWS' else ''
    InstancePublicIPv4 = ec2_metadata.public_ipv4 if env_infrastruct == 'AWS' else ''

    def get_instance_data(self)->dict:
        data = {
            "aws_region": self.instance_location_region(self.InstanceLocationRegion),
            "instance_id": self.InstanceId,
            "instance_location_region": self.InstanceLocationRegion,
            "instance_public_ipv4": self.InstancePublicIPv4,
        }
        return data
    

    def instance_location_region(self, region: str) -> str:
        region_code = region.split('-')[0]
        if not region_code: region_code ='eu'
        return AWSRegion[region_code].value
