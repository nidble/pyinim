import json
from types import SimpleNamespace

from pyinim.cloud.types.token import Token
from pyinim.cloud.types.devices import Devices

API_CLOUD_BASEURL="https://api.inimcloud.com"

class CloudResolver:
    def __init__(self, username, password, client_id):
        self.password = password
        self.username = username
        self.client_id = client_id

    def get_token_url(self):
        return f'{API_CLOUD_BASEURL}?req={{"Node":"","Name":"AlienMobilePro","ClientIP":"","Method":"RegisterClient","ClientId":"","Token":"","Params":{{"Username":"{self.username}","Password":"{self.password}","ClientId":"{self.client_id}","ClientName":"GalaxyS7edge","ClientInfo":"{{"name":"com.inim.alienmobile","version":"3.1.0","device":"hero2lte","brand":"samsung","platform":"android","osversion":"Oreo+v8.0,+API+Level:+26"}}","Role":"1","Brand":"0"}}}}'

    def get_devices_extended_url(self, token):
        return f'{API_CLOUD_BASEURL}?req={{"Params":{{"Info":4223}},"Node":"","Name":"Inim Home","ClientIP":"","Method":"GetDevicesExtended","Token":"{token}","ClientId": "{self.client_id}","Context":"intrusion"}}'

    def get_request_poll_url(self, token, device_id):
        return  f'{API_CLOUD_BASEURL}?req={{"Params":{{"DeviceId":{device_id},"Type":5}},"Node":"","Name":"Inim Home","ClientIP":"","Method":"RequestPoll","Token":"{token}","ClientId":"{self.client_id}","Context":"intrusion"}}'

    def get_activate_scenario_url(self, token, device_id, scenario_id):
        return  f'{API_CLOUD_BASEURL}?req={{"Node":"","Name":"AlienMobilePro","ClientIP":"","Method":"ActivateScenario","ClientId": "{self.client_id}","Token":"{token}","Params":{{"DeviceId":"{device_id}","ScenarioId":"{scenario_id}"}}}}'
    
    def str_to_token(self, data: str):
        token: Token = json.loads(data, object_hook=lambda d: SimpleNamespace(**d))
        return token
    
    def str_to_devices(self, data: str, device_id: str):
        devices: Devices = json.loads(data, object_hook=lambda d: SimpleNamespace(**d))
        update = { device_id: getattr(devices.Data, device_id) }
        devices.Data = dict()
        devices.Data.update(**update) 

        return devices
