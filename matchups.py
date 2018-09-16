import os
from client import Client

dir_path = os.path.dirname(os.path.realpath(__file__))
matchups_path = "data/matchups.json"
data_path = os.path.join(dir_path, matchups_path)

client = Client(data_path)
client.run()
