config = {
  "interfaces": {
    "google.ads.googleads.v6.services.KeywordPlanService": {
      "retry_codes": {
        "retry_policy_1_codes": [
          "UNAVAILABLE",
          "DEADLINE_EXCEEDED"
        ],
        "no_retry_codes": []
      },
      "retry_params": {
        "retry_policy_1_params": {
          "initial_retry_delay_millis": 5000,
          "retry_delay_multiplier": 1.3,
          "max_retry_delay_millis": 60000,
          "initial_rpc_timeout_millis": 3600000,
          "rpc_timeout_multiplier": 1.0,
          "max_rpc_timeout_millis": 3600000,
          "total_timeout_millis": 3600000
        },
        "no_retry_params": {
          "initial_retry_delay_millis": 0,
          "retry_delay_multiplier": 0.0,
          "max_retry_delay_millis": 0,
          "initial_rpc_timeout_millis": 0,
          "rpc_timeout_multiplier": 1.0,
          "max_rpc_timeout_millis": 0,
          "total_timeout_millis": 0
        }
      },
      "methods": {
        "GetKeywordPlan": {
          "timeout_millis": 60000,
          "retry_codes_name": "retry_policy_1_codes",
          "retry_params_name": "retry_policy_1_params"
        },
        "MutateKeywordPlans": {
          "timeout_millis": 60000,
          "retry_codes_name": "retry_policy_1_codes",
          "retry_params_name": "retry_policy_1_params"
        },
        "GenerateForecastCurve": {
          "timeout_millis": 3600000,
          "retry_codes_name": "retry_policy_1_codes",
          "retry_params_name": "retry_policy_1_params"
        },
        "GenerateForecastTimeSeries": {
          "timeout_millis": 3600000,
          "retry_codes_name": "retry_policy_1_codes",
          "retry_params_name": "retry_policy_1_params"
        },
        "GenerateForecastMetrics": {
          "timeout_millis": 3600000,
          "retry_codes_name": "retry_policy_1_codes",
          "retry_params_name": "retry_policy_1_params"
        },
        "GenerateHistoricalMetrics": {
          "timeout_millis": 3600000,
          "retry_codes_name": "retry_policy_1_codes",
          "retry_params_name": "retry_policy_1_params"
        }
      }
    }
  }
}
