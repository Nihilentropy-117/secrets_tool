# secrets-tool

Fetch secrets from environment variables or [Bitwarden Secrets Manager](https://bitwarden.com/products/secrets-manager/), with configurable priority and transparent fallback.

## Install

```
pip install git+https://github.com/Nihilentropy-117/secrets_tool.git
```

## Usage

```python
from secrets_tool import Secrets

secrets = Secrets()                    # env first, BWS fallback
secrets = Secrets(source="bws")        # BWS first, env fallback
secrets = Secrets(enable_bws=False)    # env only

val = secrets.get("MY_API_KEY")
val = secrets.get("MY_API_KEY", project="project-uuid")
```

`get()` raises `KeyError` if the secret is not found in any source.

## Environment variables

| Variable | Required | Default | Description |
|---|---|---|---|
| `BWS_ACCESS_TOKEN` | Yes (for BWS) | — | Bitwarden Secrets Manager machine account token |
| `BWS_ORG_ID` | Yes (for BWS) | `""` | Bitwarden organization ID |
| `BWS_API_URL` | No | `https://api.bitwarden.com` | API endpoint (self-hosted) |
| `BWS_IDENTITY_URL` | No | `https://identity.bitwarden.com` | Identity endpoint (self-hosted) |

If `BWS_ACCESS_TOKEN` is not set, BWS lookups silently return `None` and the fallback source is tried instead.

## Caching

BWS secret values are cached in memory for the lifetime of the `Secrets` instance. Create a new instance to force a refresh.
