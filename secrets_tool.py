import os
from bitwarden_sdk import BitwardenClient, DeviceType, client_settings_from_dict


class Secrets:
    def __init__(self, source: str = "env", enable_bws: bool = True):
        self._source = source
        self._enable_bws = enable_bws
        self._client = None
        self._cache = {}

    def _bws_client(self) -> BitwardenClient | None:
        if not self._enable_bws:
            return None
        if self._client is None:
            token = os.environ.get("BWS_ACCESS_TOKEN")
            if not token:
                return None
            self._client = BitwardenClient(client_settings_from_dict({
                "apiUrl": os.environ.get("BWS_API_URL", "https://api.bitwarden.com"),
                "identityUrl": os.environ.get("BWS_IDENTITY_URL", "https://identity.bitwarden.com"),
                "deviceType": DeviceType.SDK,
                "userAgent": "Python",
            }))
            self._client.access_token_login(token)
        return self._client

    def _from_env(self, name: str) -> str | None:
        return os.environ.get(name)

    def _from_bws(self, name: str, project: str | None = None) -> str | None:
        key = (name, project)
        if key in self._cache:
            return self._cache[key]
        client = self._bws_client()
        if not client:
            return None
        org_id = os.environ.get("BWS_ORG_ID", "")
        for s in client.secrets().list(org_id).data.data:
            if s.key == name and (project is None or s.project_id == project):
                self._cache[key] = client.secrets().get(s.id).data.value
                return self._cache[key]
        return None

    def get(self, name: str, project: str | None = None) -> str:
        first, second = (self._from_env, self._from_bws) if self._source == "env" else (self._from_bws, self._from_env)
        val = first(name, project) if first == self._from_bws else first(name)
        if val is not None:
            return val
        val = second(name, project) if second == self._from_bws else second(name)
        if val is not None:
            return val
        raise KeyError(f"Secret '{name}' not found")
