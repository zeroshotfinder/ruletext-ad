from litellm import cost_per_token
import litellm
from environment import calculate_carbon_track
from typing import Optional, Dict
from datetime import datetime, timezone, timedelta


############################
# Describe here new models #
############################
llama_4_scout = {
    "groq/llama-4-scout-17b-16e-instruct": {
        "max_tokens": 8192,
        "input_cost_per_token": 0.11 /  1e6,
        "output_cost_per_token": 0.34 / 1e6 ,
        "litellm_provider": "groq",
        "mode": "chat"
    }
}

llama_4_maverick = {
    "groq/llama-4-maverick-17b-128e-instruct": {
        "max_tokens": 8192,
        "input_cost_per_token": 0.20 / 1e6,
        "output_cost_per_token": 0.60 / 1e6,
        "litellm_provider": "groq",
        "mode": "chat"
    }
}

litellm.register_model(llama_4_scout)
litellm.register_model(llama_4_maverick)

class Billing:
    def __init__(self, headers: Dict[str, str], body: Dict[str, str]):
        self.cost: Optional[float] = self._parse_float(headers.get("x-litellm-response-cost"))
        self.key_spend: Optional[float] = self._parse_float(headers.get("x-litellm-key-spend"))
        self.proxy_request_id: Optional[str] = body.get('id')
        self.created: Optional[str] = self._parse_unix_time(body.get('created'))
        self.raw_headers: Dict[str, str] = headers

    @staticmethod
    def _parse_float(value: Optional[str]) -> Optional[float]:
        try:
            return float(value) if value is not None else None
        except ValueError:
            return None

    @staticmethod
    def _parse_unix_time(value: int) -> Optional[str]:
        try:
            dt_utc = datetime.fromtimestamp(value, tz=timezone.utc)
            return dt_utc.astimezone(timezone(timedelta(hours=-3))).isoformat()
        except ValueError:
            return None

    def to_dict(self) -> Dict[str, Optional[str]]:
        return {
            "cost": self.cost,
            "key_spend": self.key_spend,
            "proxy_request_id": self.proxy_request_id,
            "created": self.created
        }

# Source: https://docs.litellm.ai/docs/completion/token_usage
def cost_per_token_calculator(usage_metadata, llm) -> dict:        
        output_tokens = usage_metadata.response_tokens + usage_metadata.details.get('thoughts_tokens', 0) if usage_metadata.details else usage_metadata.response_tokens
        total_tokens = usage_metadata.request_tokens + output_tokens
        return {            
            'input_tokens': usage_metadata.request_tokens,
            'output_tokens': output_tokens,
            'total_tokens':total_tokens
        }

def calculate_all_costs(usage_metadata, total_images, provider, llm):
    cost_per_tokens  = cost_per_token_calculator(usage_metadata, llm)
    energy_kwh, co2_kg = calculate_carbon_track(provider, cost_per_tokens['total_tokens'])
    cost_per_tokens |= {
        'provider': provider,
        'model': llm,
        'total_prompt_images': total_images,
        'energy_kwh': energy_kwh,
        'co2_kg': co2_kg
    }
    return cost_per_tokens