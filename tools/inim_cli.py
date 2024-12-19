#!/usr/bin/env python3
import argparse
import asyncio
import json
import sys
import uuid

import aiohttp

# Add the src directory to the PyInim path
sys.path.append("../src")

from pyinim.inim_cloud import InimCloud  # correct this import

POINTER = "❯"
POINTER_R = "❮"
BRIGHT_RED = "\033[31m"
LIGHT_RED = "\033[91m"
BRIGHT_GREEN = "\033[32m"
LIGHT_GREEN = "\033[92m"
BRIGHT_YELLOW = "\033[33m"
LIGHT_YELLOW = "\033[93m"
BRIGHT_BLUE = "\033[34m"
LIGHT_BLUE = "\033[94m"
BRIGHT_MAGENTA = "\033[35m"
LIGHT_MAGENTA = "\033[95m"
BOLD = "\033[1m"
RESET = "\033[0m"


async def poc():
    parser = argparse.ArgumentParser()
    parser.add_argument("--username", help="Inim User Name")
    parser.add_argument("--password", help="Inim Password")
    parser.add_argument("--client_id", help="Inim Client ID")
    parser.add_argument(
        "--list",
        choices=["deviceid", "areas", "scenarios"],  # Added "scenarios"
        required=True,
        help="Specify whether to list 'deviceid', 'areas', or 'scenarios'",
    )
    parser.add_argument(
        "--deviceid",
        help="Optional device ID to filter results for 'areas' and 'scenarios'",
    )
    parser.add_argument(
        "--dump",
        metavar="filename",
        help="Dump the raw JSON response to the specified file",
    )
    args = parser.parse_args()

    username = args.username
    password = args.password
    client_id = args.client_id or str(uuid.uuid4())

    # Check if values are empty and exit with error if so
    if not all([username, password, client_id]):
        print(
            "Error: Missing required arguments or environment variables. Please provide username and password."
        )
        sys.exit(1)

    async with aiohttp.ClientSession() as session:
        inim = InimCloud(
            session,
            name="poc",
            username=username,
            password=password,
            client_id=client_id,
        )
        _st, _hs, devices_resp = await inim.get_devices_list()

        # Dump JSON to file if --dump is specified
        if args.dump:
            try:
                with open(args.dump, "w") as f:
                    json.dump(devices_resp, f, indent=4)
                print(f"JSON response dumped to {args.dump}")
            except Exception as e:
                print(f"Error dumping JSON to file: {e}")

        if args.list == "deviceid":
            extract_device_info(devices_resp)
        elif args.list == "areas":
            extract_areas_id(devices_resp, args.deviceid)
        elif args.list == "scenarios":  # Added "scenarios" branch
            extract_scenarios_id(devices_resp, args.deviceid)


def extract_device_info(devices_list):
    # data = json.dumps(devices_list)
    devices = devices_list.get("Data", {})
    for device_id, device_data in devices.items():
        device_id_str = "DeviceId: "
        device_id_value_str = f"{device_data.get('DeviceId')}"
        name_str = "Name: "
        name_value_str = f"{device_data.get('Name')}"
        serial_number_str = "SerialNumber: "
        serial_number_value_str = f"{device_data.get('SerialNumber')}"
        model_family_str = "ModelFamily: "
        model_family_value_str = f"{device_data.get('ModelFamily')}"
        model_number_str = "ModelNumber: "
        model_number_value_str = f"{device_data.get('ModelNumber')}"

        print(
            f"{BRIGHT_RED}{device_id_str}{RESET}{BOLD}{LIGHT_RED}{POINTER}{RESET}{BOLD} {device_id_value_str} {LIGHT_RED}{POINTER_R}{RESET}, "
            f"{BRIGHT_GREEN}{name_str}{RESET}{LIGHT_GREEN}{name_value_str}{RESET}, "
            f"{BRIGHT_YELLOW}{serial_number_str}{RESET}{LIGHT_YELLOW}{serial_number_value_str}{RESET}, "
            f"{BRIGHT_BLUE}{model_family_str}{RESET}{LIGHT_BLUE}{model_family_value_str}{RESET}, "
            f"{BRIGHT_MAGENTA}{model_number_str}{RESET}{LIGHT_MAGENTA}{model_number_value_str}{RESET}"
        )


def extract_areas_id(data, device_id=None):
    for data_key, device_data in data["Data"].items():
        if device_id is not None and data_key != device_id:
            continue  # Skip if device ID doesn't match

        print(
            f"{BRIGHT_RED}Device ID:{RESET}{BOLD}{LIGHT_RED}{POINTER}{RESET}{BOLD} {data_key} {LIGHT_RED}{POINTER_R}{RESET}"
        )
        for area in device_data["Areas"]:
            print(
                f"  {BRIGHT_GREEN}Area ID:{RESET}{LIGHT_GREEN}{area['AreaId']}{RESET}, {BRIGHT_BLUE}Name: {RESET}{LIGHT_BLUE}{area['Name']}{RESET}"
            )


def extract_scenarios_id(data, device_id=None):
    for data_key, device_data in data["Data"].items():
        if device_id is not None and data_key != device_id:
            continue  # Skip if device ID doesn't match

        print(
            f"{BRIGHT_RED}Device ID:{RESET}{BOLD}{LIGHT_RED}{POINTER}{RESET}{BOLD} {data_key} {LIGHT_RED}{POINTER_R}{RESET}"
        )
        for scenario in device_data["Scenarios"]:
            print(
                f"  {BRIGHT_GREEN}Scenario ID:{RESET}{LIGHT_GREEN}{scenario['ScenarioId']}{RESET}, {BRIGHT_BLUE}Name: {RESET}{LIGHT_BLUE}{scenario['Name']}{RESET}"
            )


async def main():
    await poc()


asyncio.run(main())
