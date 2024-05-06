import aiohttp
import asyncio
import os
from dotenv import load_dotenv

from pyinim.inim_cloud import InimCloud

load_dotenv()
INIM_USER = os.getenv('INIM_USER')
INIM_PASSWORD = os.getenv('INIM_PASSWORD')
INIM_CLIENT_ID = os.getenv('INIM_CLIENT_ID')
INIM_DEVICE_ID = os.getenv('INIM_DEVICE_ID')

def print_device_extended(devices_extended):
    print("Devices Extended: Name {}, DeviceId: {}, ActiveScenario: {}, ActiveScenarios: {}, Master: {},  Enabled: {}, NetworkStatus: {}".format(
        devices_extended.Name, devices_extended.DeviceId, devices_extended.ActiveScenario, devices_extended.ActiveScenarios, devices_extended.Enabled, devices_extended.Master, devices_extended.NetworkStatus
    ))
    for scenario in devices_extended.Scenarios:
        print("Scenario: {}, Id: {}, AreaSet: {}, AreaMask: {}, Icona: {}, Uscita: {}".format(scenario.Name, scenario.ScenarioId, scenario.AreaSet, scenario.AreaMask, scenario.Icona, scenario.Uscita))

async def poc():
    async with aiohttp.ClientSession() as session:
        inim = InimCloud(session, name="poc", username=INIM_USER, password=INIM_PASSWORD, client_id=INIM_CLIENT_ID)
        await inim.get_request_poll(INIM_DEVICE_ID)
        _st, _hs, devices_resp = await inim.get_devices_extended(INIM_DEVICE_ID)

        print_device_extended(devices_resp.Data[INIM_DEVICE_ID])

async def main():
    await poc()

asyncio.run(main())
