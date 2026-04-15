import json
from types import SimpleNamespace
from pyinim.cloud.types.token import Token
from pyinim.cloud.types.devices import Devices

API_CLOUD_BASEURL = "https://api.inimcloud.com"
ENABLE_BYPASS_MODE = 3
DISABLE_BYPASS_MODE = 0


class CloudResolver:
    def __init__(self, username, password, client_id, code):
        self.password = password
        self.username = username
        self.client_id = client_id
        self.code = code

    def get_token_url(self):
        data = {
            "Node": "",
            "Name": "AlienMobilePro",
            "ClientIP": "",
            "Method": "RegisterClient",
            "ClientId": "",
            "Token": "",
            "Params": {
                "Username": f"{self.username}",
                "Password": f"{self.password}",
                "ClientId": f"{self.client_id}",
                "ClientName": "Galaxy+S8+edge",
                "ClientInfo": json.dumps(
                    {
                        "name": "com.inim.alienmobile",
                        "version": "3.1.0",
                        "device": "hero2lte",
                        "brand": "samsung",
                        "platform": "android",
                        "osversion": "Oreo+v8.0,+API+Level:+26",
                    }
                ),
                "Role": "1",
                "Brand": "0",
            },
        }
        return f"{API_CLOUD_BASEURL}?req={json.dumps(data)}"

    def get_devices_extended_url(self, token):
        return f'{API_CLOUD_BASEURL}?req={{"Params":{{"Info":4223}},"Node":"","Name":"Inim Home","ClientIP":"","Method":"GetDevicesExtended","Token":"{token}","ClientId": "{self.client_id}","Context":"intrusion"}}'

    def get_enable_bypass_zone(self, token, device_id, zone_id):
        return self.__get_bypass_zone(token, device_id, zone_id, ENABLE_BYPASS_MODE)

    def get_disable_bypass_zone(self, token, device_id, zone_id):
        return self.__get_bypass_zone(token, device_id, zone_id, DISABLE_BYPASS_MODE)

    def __get_bypass_zone(self, token, device_id, zone_id, bypass_mode):
        return f'{API_CLOUD_BASEURL}?req={{"Node":"","Name":"AlienMobilePro","ClientIP":"","Method":"InsertZone","ClientId":"{self.client_id}","Token":"{token}","Params":{{"DeviceId":"{device_id}","ZoneId":{zone_id},"Value":0,"Mode":{bypass_mode},"Code":"{self.code}"}}}}'

    def get_request_poll_url(self, token, device_id):
        return f'{API_CLOUD_BASEURL}?req={{"Params":{{"DeviceId":{device_id},"Type":5}},"Node":"","Name":"Inim Home","ClientIP":"","Method":"RequestPoll","Token":"{token}","ClientId":"{self.client_id}","Context":"intrusion"}}'

    def get_activate_scenario_url(self, token, device_id, scenario_id):
        return f'{API_CLOUD_BASEURL}?req={{"Node":"","Name":"AlienMobilePro","ClientIP":"","Method":"ActivateScenario","ClientId": "{self.client_id}","Token":"{token}","Params":{{"DeviceId":"{device_id}","ScenarioId":"{scenario_id}"}}}}'

    def str_to_token(self, data: str):
        token: Token = json.loads(data, object_hook=lambda d: SimpleNamespace(**d))
        return token

    def str_to_devices(self, data: str, device_id: str):
        devices: Devices = json.loads(data, object_hook=lambda d: SimpleNamespace(**d))
        update = {device_id: getattr(devices.Data, device_id)}
        devices.Data = dict()
        devices.Data.update(**update)

        return devices

    def str_to_devices_list(self, data: str) -> dict[str, Devices]:
        devices: Devices = json.loads(data)
        return devices
