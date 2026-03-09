from __future__ import annotations

from ..transport import HTTPTransport
from .companies import AdminCompaniesAPI
from .crm import AdminCrmAPI
from .environments import AdminEnvironmentsAPI
from .mappings import AdminMappingsAPI
from .partners import AdminPartnersAPI
from .powerbi import AdminPowerBIAPI
from .sync import AdminSyncAPI
from .sync_source_definitions import AdminSyncSourceDefinitionsAPI


class AdminClient:
    def __init__(self, transport: HTTPTransport) -> None:
        """Initialize grouped admin endpoint clients."""
        self.companies = AdminCompaniesAPI(transport)
        self.crm = AdminCrmAPI(transport)
        self.environments = AdminEnvironmentsAPI(transport)
        self.mappings = AdminMappingsAPI(transport)
        self.partners = AdminPartnersAPI(transport)
        self.powerbi = AdminPowerBIAPI(transport)
        self.sync = AdminSyncAPI(transport)
        self.sync_source_definitions = AdminSyncSourceDefinitionsAPI(transport)
