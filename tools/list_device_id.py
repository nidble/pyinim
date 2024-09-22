#!/usr/bin/env python3
import aiohttp
import asyncio
import os
import sys
from dotenv import load_dotenv
import argparse
import uuid
import json

# Add the src directory to the PyInim path
sys.path.append("../src")

from pyinim.inim_cloud import InimCloud  # correct this import
from types import SimpleNamespace

load_dotenv()

INIM_USER = os.getenv("INIM_USER")
INIM_PASSWORD = os.getenv("INIM_PASSWORD")
INIM_CLIENT_ID = os.getenv("INIM_CLIENT_ID")

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
    args = parser.parse_args()

    # Use arguments if provided, otherwise fall back to environment variables
    username = args.username or INIM_USER
    password = args.password or INIM_PASSWORD
    client_id = args.client_id or INIM_CLIENT_ID or str(uuid.uuid4())

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
            username=args.username
            or INIM_USER,  # Use argument if provided, otherwise default
            password=args.password
            or INIM_PASSWORD,  # Use argument if provided, otherwise default
            client_id=INIM_CLIENT_ID,
        )
        _st, _hs, devices_resp = await inim.get_devices_list()
        extract_device_info(devices_resp)


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


# Example usage:


async def main():
    await poc()


asyncio.run(main())
