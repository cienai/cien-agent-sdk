from unittest.mock import Mock

from cien_agent_sdk.admin.runtime_model_performance import AdminRuntimeModelPerformanceAPI


def test_runtime_model_performance_save_posts_metrics():
    api = AdminRuntimeModelPerformanceAPI.__new__(AdminRuntimeModelPerformanceAPI)
    api._transport = Mock()
    api._transport.request.return_value = {"_sys_doc_id": "run-1"}

    result = api.save({"model_name": "industry"})

    assert result == {"_sys_doc_id": "run-1"}
    api._transport.request.assert_called_once_with(
        "POST", "/api/admin/runtime-model-performance", json={"model_name": "industry"}
    )
