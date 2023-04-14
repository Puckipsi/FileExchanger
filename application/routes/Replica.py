from __init__ import app
from utils.config import Config
from application.services.CrosReplica.Replica import FileReplica

config = Config()
file_replica = FileReplica()


app.add_url_rule(
    rule=f"/{config.get_replicate_file_endpoint()}/<filename>", methods=["GET"], view_func=file_replica.replicate_file)
