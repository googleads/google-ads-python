config = {
  "interfaces": {
    "google.ads.googleads.v6.services.CampaignExperimentService": {
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
        "GetCampaignExperiment": {
          "timeout_millis": 3600000,
          "retry_codes_name": "retry_policy_1_codes",
          "retry_params_name": "retry_policy_1_params"
        },
        "CreateCampaignExperiment": {
          "timeout_millis": 3600000,
          "retry_codes_name": "retry_policy_1_codes",
          "retry_params_name": "retry_policy_1_params"
        },
        "MutateCampaignExperiments": {
          "timeout_millis": 3600000,
          "retry_codes_name": "retry_policy_1_codes",
          "retry_params_name": "retry_policy_1_params"
        },
        "GraduateCampaignExperiment": {
          "timeout_millis": 3600000,
          "retry_codes_name": "retry_policy_1_codes",
          "retry_params_name": "retry_policy_1_params"
        },
        "PromoteCampaignExperiment": {
          "timeout_millis": 3600000,
          "retry_codes_name": "retry_policy_1_codes",
          "retry_params_name": "retry_policy_1_params"
        },
        "EndCampaignExperiment": {
          "timeout_millis": 3600000,
          "retry_codes_name": "retry_policy_1_codes",
          "retry_params_name": "retry_policy_1_params"
        },
        "ListCampaignExperimentAsyncErrors": {
          "timeout_millis": 3600000,
          "retry_codes_name": "retry_policy_1_codes",
          "retry_params_name": "retry_policy_1_params"
        }
      }
    }
  }
}
