config = {
  "interfaces": {
    "google.ads.googleads.v2.services.CustomerFeedService": {
      "retry_codes": {
        "idempotent": [
          "DEADLINE_EXCEEDED",
          "UNAVAILABLE"
        ],
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
        "GetCustomerFeed": {
          "timeout_millis": 60000,
          "retry_codes_name": "idempotent",
          "retry_params_name": "default"
        },
        "MutateCustomerFeeds": {
          "timeout_millis": 60000,
          "retry_codes_name": "non_idempotent",
          "retry_params_name": "default"
        }
      }
    }
  }
}
