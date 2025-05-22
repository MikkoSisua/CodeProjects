import requests
from typing import Dict, Any, List

class OrchestratorClient:
    def __init__(self, config: Dict[str, Any]):
        self.base_url = config['orchestrator']['url'].rstrip('/')
        self.tenant = config['orchestrator'].get('tenant', '')
        self.client_id = config['orchestrator']['client_id']
        self.user_key = config['orchestrator']['user_key']
        self.refresh_token = config['orchestrator']['refresh_token']
        self.access_token = None

    def authenticate(self) -> str:
        url = f"{self.base_url}/api/account/authenticate"
        data = {
            'tenancyName': self.tenant,
            'clientId': self.client_id,
            'refreshToken': self.refresh_token
        }
        resp = requests.post(url, json=data)
        resp.raise_for_status()
        self.access_token = resp.json().get('access_token')
        return self.access_token

    def _headers(self) -> Dict[str, str]:
        if not self.access_token:
            self.authenticate()
        return {
            'Authorization': f'Bearer {self.access_token}',
            'X-UIPATH-OrganizationUnitId': '0'
        }

    def get_folders(self) -> List[Dict[str, Any]]:
        url = f"{self.base_url}/odata/Folders"
        resp = requests.get(url, headers=self._headers())
        resp.raise_for_status()
        return resp.json().get('value', [])

    def get_triggers(self, folder_id: int) -> List[Dict[str, Any]]:
        url = f"{self.base_url}/odata/ProcessSchedules?$filter=FolderId eq {folder_id}"
        resp = requests.get(url, headers=self._headers())
        resp.raise_for_status()
        return resp.json().get('value', [])
