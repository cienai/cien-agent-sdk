from __future__ import annotations

from ..transport import HTTPTransport
from .companies import PublicCompaniesAPI
from .config import PublicConfigAPI
from .powerbi import PublicPowerBIAPI
from .user_company_permissions import PublicUserCompanyPermissionsAPI
from .users import PublicUsersAPI
from .version import PublicVersionAPI


class PublicClient:
    def __init__(self, transport: HTTPTransport) -> None:
        self.companies = PublicCompaniesAPI(transport)
        self.config = PublicConfigAPI(transport)
        self.powerbi = PublicPowerBIAPI(transport)
        self.user_company_permissions = PublicUserCompanyPermissionsAPI(transport)
        self.users = PublicUsersAPI(transport)
        self.version = PublicVersionAPI(transport)
