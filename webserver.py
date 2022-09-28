import argparse
from flask import Flask, request
import json
import os
import socket
import asyncio
from threading import Thread
from mdns_beacon import Beacon
from ipaddress import ip_address

app = Flask(__name__)
json_file = "json/wiser.json"
json_data = {}
json_section = "data"

def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(0)
    try:
        # doesn't even have to be reachable
        s.connect(('10.254.254.254', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

def start_mdns_broadcaster(loop):
    asyncio.set_event_loop(loop)
    local_ip = get_ip()
    print(f"IP Address is {local_ip}")
    print("Starting MDNS broadcast")
    beacon = Beacon(
        aliases=["WiserHeatXXXXXX"],
        addresses=list([ip_address(local_ip)]),
        port=80,
        type_="http",
        protocol="tcp",
        weight=0,
        priority=0,
        properties=b"",
        delay_startup=0,
    )
    beacon.run_forever()

def main_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description='A mock Wiser Hub server for testing of different setups')
    parser.add_argument("-d", "--dir", help="Direcory of a wiser diagnostic file.", default="json")
    return parser

def validate_json_dir(path: str):
    try:
        data_file = [filename for filename in os.listdir(path) if filename.endswith(".json")]

        if not data_file:
            print(f"The directory {path} does not contain a hub data file.  Please check the path supplied.")
            return None
        return data_file[0]
    except FileNotFoundError:
        print(f"The directory {path} does not exist.  Please check the path supplied.")

@app.after_request
def set_header(response):
    response.headers["Content-Type"] = "application/json"
    return response

@app.route('/data/v2/domain/', methods=['GET'])
def domain():
    return json.dumps(json_data.get("Domain"))

@app.route('/data/v2/network/', methods=['GET'])
def network():
    return json.dumps(json_data.get("Network"))

@app.route('/data/v2/schedules/', methods=['GET'])
def scheudles():
    return json.dumps(json_data.get("Schedule"))

@app.route('/data/v2/opentherm/', methods=['GET'])
def opentherm():
    return json.dumps(json_data.get("OpenTherm"))

# Dummy endpoints for updates
@app.route('/data/v2/domain/<path>/<id>', methods=['PATCH'])
@app.route('/data/v2/domain/<path>/', methods=['PATCH'])
@app.route('/data/v2/schedules/<path>', methods=['PATCH','POST','DELETE'])
@app.route('/data/v2/schedules/<path>/<id>', methods=['PATCH','POST','DELETE'])
def patch_device(path: str="", id: str=""):
    print(request.data)
    return request.data

def main():
    global json_data
    parser = main_parser()
    args = parser.parse_args()
    json_file = validate_json_dir(args.dir)
    if json_file:
        f = open(f"{args.dir}/{json_file}")
        json_data = json.loads(f.read()).get("data")
        print(f"Using json files from {json_file}")

        loop = asyncio.new_event_loop()
        t = Thread(target=start_mdns_broadcaster, args=(loop,), daemon=True)
        t.start()

        print("Starting Webserver...")
        app.run(host="0.0.0.0", port=80)

if __name__ == '__main__':
    main()
