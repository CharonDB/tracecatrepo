from typing import Annotated, Any
from pydantic import Field
from tracecat_registry import registry, RegistrySecret, secrets
import httpx


heimdall_secret = RegistrySecret(
    name = "heimdall",
    keys = ["HEIMDALL_API_KEY", "HEIMDALL_CUSTOMER_ID"],)

@registry.register(
    default_title="Get DarkLayer alerts",
    display_group="Heimdall - DarkLayer",
    description="Get Heimdall alerts",
    namespace="integrations.heimdall.darklayer",
    secrets=[heimdall_secret],
)

async def get_darklayer_alerts() -> dict[str, Any]:
    clientInfoId: Annotated[int | None, Field(description="The client ID (in case of querying a specific client)")]

    api_key = await secrets.get("HEIMDALL_API_KEY")
    customer_id = await secrets.get("HEIMDALL_CUSTOMER_ID")
    if secret is None:
        raise ValueError("Failed to retrieve 'heimdall' secret")

    uri = "https://rc-dashboard.heimdalsecurity.com/api/heimdalapi/darklayerguard"
    async with httpx.AsyncClient() as client:
        response = await client.get(
            uri, 
            headers={"Authorization": "Bearer "+api_key},
            params={"customerid": customer_id}
        )
        response.raise_for_status()
        return response.json()
    
                                                       
