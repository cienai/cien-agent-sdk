from __future__ import annotations

from typing import Any

from ..base import EndpointGroup


class AdminThirdPartyServicesAPI(EndpointGroup):
    """Platform service roles resolved through the scoped third-party service registry."""

    def prepare_service(self, role: str, *, co_id: str, include_credential: bool = False) -> dict[str, Any]:
        """Resolve a platform ``role`` (``platform_embedding``, ``geocoding``) to its effective service for ``co_id``.

        Returns the same service identity as a Model Definition receipt (``service_id``, ``service_doc_id``,
        ``service_revision``, ``vendor``, ``model_id``, ``auth_mode``, ``settings`` and the pricing version). With
        ``include_credential`` it also carries ``credential`` (pipeline API keys only; never log or persist it).
        An unknown role raises ``APIError`` (404); an unavailable, inactive or uncredentialed service 409.
        Never cached: the receipt identifies the executed service version.
        """
        return self._transport.request("GET", f"/api/admin/third-party-services/system/{role}/execution",
                                       headers={"x-cien-coid": str(co_id)},
                                       params={"include_credential": "true"} if include_credential else None)
