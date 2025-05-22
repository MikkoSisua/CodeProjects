import msal
from flask import session
from typing import Dict, Any

class MSAuth:
    def __init__(self, config: Dict[str, Any]):
        self.client_id = config['aad']['client_id']
        self.client_secret = config['aad']['client_secret']
        self.authority = f"https://login.microsoftonline.com/{config['aad']['tenant_id']}"
        self.scope = ['User.Read']
        self.app = msal.ConfidentialClientApplication(
            self.client_id,
            authority=self.authority,
            client_credential=self.client_secret
        )

    def build_auth_url(self, redirect_uri: str, state: str):
        return self.app.get_authorization_request_url(self.scope, state=state, redirect_uri=redirect_uri)

    def acquire_token_by_authorization_code(self, code: str, redirect_uri: str):
        return self.app.acquire_token_by_authorization_code(code, scopes=self.scope, redirect_uri=redirect_uri)

    def get_token_silent(self):
        accounts = self.app.get_accounts()
        if accounts:
            result = self.app.acquire_token_silent(self.scope, account=accounts[0])
            return result
        return None
