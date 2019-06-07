config = {
    "interfaces": {
        "google.ads.googleads.v1.services.KeywordPlanService": {
            "retry_codes": {
                "idempotent": ["DEADLINE_EXCEEDED", "UNAVAILABLE"],
                "non_idempotent": []
            },
            "retry_params": {
                "default": {
                    "initial_retry_delay_millis": 5000,
                    "retry_delay_multiplier": 1.3,
                    "max_retry_delay_millis": 60000,
                    "initial_rpc_timeout_millis": 3600000,
                    "rpc_timeout_multiplier": 1.0,
                    "max_rpc_timeout_millis": 3600000,
                    "total_timeout_millis": 3600000
                }
            },
            "methods": {
                "GetKeywordPlan": {
                    "timeout_millis": 60000,
                    "retry_codes_name": "idempotent",
                    "retry_params_name": "default"
                },
                "MutateKeywordPlans": {
                    "timeout_millis": 60000,
                    "retry_codes_name": "non_idempotent",
                    "retry_params_name": "default"
                },
                "GenerateForecastMetrics": {
                    "timeout_millis": 600000,
                    "retry_codes_name": "idempotent",
                    "retry_params_name": "default"
                },
                "GenerateHistoricalMetrics": {
                    "timeout_millis": 600000,
                    "retry_codes_name": "idempotent",
                    "retry_params_name": "default"
                }
            }
        }
    }
}
