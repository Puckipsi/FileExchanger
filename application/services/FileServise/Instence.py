from ec2_metadata import ec2_metadata
from dotenv import dotenv_values


config = dotenv_values('.env')
env_infrastruct = config['ENVIRONMENT_INFRASTRUCT']


class EC2Instance:

    InstanceId = ec2_metadata.instance_id if env_infrastruct == 'AWS' else ''
    InstanceLocationRegion = ec2_metadata.region if env_infrastruct == 'AWS' else ''
    InstancePublicIPv4 = ec2_metadata.public_ipv4 if env_infrastruct == 'AWS' else ''

    def get_instance_data(self)->dict:
        data = {
            "instance_id": self.InstanceId,
            "instance_location_region": self.InstanceLocationRegion,
            "instance_public_ipv4": self.InstancePublicIPv4,
        }
        return data