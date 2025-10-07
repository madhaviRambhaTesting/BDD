import configparser
import os

config = configparser.ConfigParser()

config_path = os.path.join(os.path.dirname(__file__), 'config.ini')
config.read(config_path)

try:
    base_url = config["Default"]["Base_URL"]
    uname = config["Default"]["Uname"]
    passwd = config["Default"]["Psed"]

    markers = config["Pytest"].get("markers", "")
    quiet_mode = config["Pytest"].getboolean("q", False)
    verbose = config["Pytest"].getboolean("v", False)
    max_fail = config["Pytest"].getint("maxfail", 1)
except KeyError as e:
    raise Exception(f"Missing configuration key: {e}. Please check your config.ini file and ensure all necessary keys are provided.")