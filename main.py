import os,json
from windy import Windy

def get_routes():
    dirname = os.path.dirname(__file__)
    config_file = os.path.join(dirname, "windy/conf/routes.json")
    json_conf = ""
    with open(config_file, "r") as f:
        json_conf = json.load(f)
    return json_conf

application=Windy(get_routes())

