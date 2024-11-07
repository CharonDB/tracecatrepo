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

async def get_darklayer_alerts(
    clientInfoId: Annotated[int | None, Field(description="The client ID (in case of querying a specific client)")],
    startDate: Annotated[str, Field(description="The start date for the query")],
    endDate: Annotated[str, Field(description="The end date for the query")]
    ) -> dict[str, Any]:


    uri = "https://rc-dashboard.heimdalsecurity.com/api/heimdalapi/darklayerguard"

    paramsjson = {
        "customerid": secrets.get("HEIMDALL_CUSTOMER_ID"),
    }

    if clientInfoId:
        paramsjson["clientinfoid"] = clientInfoId
    if startDate:
        paramsjson["startdate"] = startDate
    if endDate:
        paramsjson["enddate"] = endDate

    result = None

    async with httpx.AsyncClient() as client:
        response = await client.get(
            uri, 
            headers={"Authorization": "Bearer "+secrets.get("HEIMDALL_API_KEY")},
            params=paramsjson
        )
        response.raise_for_status()
        result = response.json()

    return result             
