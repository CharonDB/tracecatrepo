from typing import Annotated, Any
from pydantic import Field
from tracecat_registry import registry, RegistrySecret, secrets
import httpx


heimdall_secret = RegistrySecret(
    name = "heimdall",
    keys = ["HEIMDALL_API_KEY", "HEIMDALL_CUSTOMER_ID"],)


@registry.register(
    default_title="Get Heimdall alerts",
    display_group="Heimdall",
    description="Get Heimdall alerts",
    namespace="integrations.heimdall",
)
async def get_heimdall_alerts(value: str) -> dict[str, Any]:
    return "Hello, world!"

@registry.register(
    default_title="Get DarkLayer alerts",
    display_group="Heimdall - DarkLayer",
    description="Get Heimdall alerts",
    namespace="integrations.heimdall.darklayer",
    secrets=[heimdall_secret],
)
async def get_darklayer_alerts(value: str) -> dict[str, Any]:
    clientInfoId: Annotated[int | None, Field(description="The client ID (in case of querying a specific client)")]

    secret = await secrets.get("heimdall")
    uri = "https://rc-dashboard.heimdalsecurity.com/api/heimdalapi/darklayerguard"
    async with httpx.AsyncClient() as client:
        response = await client.get(
            uri, 
            headers={"Authorization": f"Bearer {secret}"},
            params={"customerid": secret["HEIMDALL_CUSTOMER_ID"]}
        )
        response.raise_for_status()
        return response.json()
    
                                                       
