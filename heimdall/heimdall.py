from typing import Annotated, Any
from pydantic import Field
from tracecat_registry import registry


@registry.register(
    default_title="Get Heimdall alerts",
    display_group="Heimdall",
    description="Get Heimdall alerts",
    namespace="integrations.heimdall",
)
async def get_heimdall_alerts(value: str) -> dict[str, Any]:
    return "Hello, world!"