from __future__ import annotations

from ..transport import HTTPTransport
from .companies import AdminCompaniesAPI
from .company_purge_and_copy_logs import AdminCompanyPurgeAndCopyLogsAPI
from .data_deletions import AdminDataDeletionsAPI
from .companies_history import AdminCompaniesHistoryAPI
from .crm import AdminCrmAPI
from .environments import AdminEnvironmentsAPI
from .jobs import AdminJobsAPI
from .job_data import AdminJobDataAPI
from .job_engine_logs import AdminJobEngineLogsAPI
from .mappings import AdminMappingsAPI
from .models_validation import AdminModelsValidationAPI
from .partners import AdminPartnersAPI
from .powerbi import AdminPowerBIAPI
from .sync import AdminSyncAPI
from .sync_live_query import AdminSyncLiveQueryAPI
from .sync_mappings import AdminSyncMappingsAPI
from .sync_source_definitions import AdminSyncSourceDefinitionsAPI


class AdminClient:
    def __init__(self, transport: HTTPTransport) -> None:
        """Initialize grouped admin endpoint clients."""
        self.companies = AdminCompaniesAPI(transport)
        self.company_purge_and_copy_logs = AdminCompanyPurgeAndCopyLogsAPI(transport)
        self.data_deletions = AdminDataDeletionsAPI(transport)
        self.companies_history = AdminCompaniesHistoryAPI(transport)
        self.crm = AdminCrmAPI(transport)
        self.environments = AdminEnvironmentsAPI(transport)
        self.jobs = AdminJobsAPI(transport)
        self.job_data = AdminJobDataAPI(transport)
        self.job_engine_logs = AdminJobEngineLogsAPI(transport)
        self.mappings = AdminMappingsAPI(transport)
        self.models_validation = AdminModelsValidationAPI(transport)
        self.partners = AdminPartnersAPI(transport)
        self.powerbi = AdminPowerBIAPI(transport)
        self.sync = AdminSyncAPI(transport)
        self.sync_live_query = AdminSyncLiveQueryAPI(transport)
        self.sync_mappings = AdminSyncMappingsAPI(transport)
        self.sync_source_definitions = AdminSyncSourceDefinitionsAPI(transport)
