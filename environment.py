"""
Refererences:
https://cloud.google.com/blog/topics/sustainability/tpus-improved-carbon-efficiency-of-ai-workloads-by-3x
https://ar5iv.labs.arxiv.org/html/2502.01671
https://epoch.ai/gradient-updates/how-much-energy-does-chatgpt-use
https://epoch.ai/gradient-updates/frontier-language-models-have-become-much-smaller
https://arxiv.org/pdf/2211.02001
"""
from typing import Tuple

# wh/tokens for providers based on research
GOOGLE_VERTEX_WH_TOKEN = 0.0002
OPEN_AI_WH_TOKEN = 0.0002
GROQ_LPU_MOE_WH_TOKEN = 0.00003

EAST_US_2_CI = 0.412
CENTRAL_US_1_CI = 0.447
# groq datacenters
# https://www.prnewswire.com/news-releases/saudi-arabia-announces-1-5-billion-expansion-to-fuel-ai-powered-economy-with-ai-tech-leader-groq-302372643.html?utm_source=chatgpt.com
DAMMAM_SAUDI_CI = 0.558

WH_TOKEN_MAPPING = {
    'google-vertex': GOOGLE_VERTEX_WH_TOKEN,
    'openai': OPEN_AI_WH_TOKEN,
    'groq': GROQ_LPU_MOE_WH_TOKEN
}

def calculate_energy(wh_token, tokens) -> float:
    return tokens * wh_token / 1000

def calculate_carbon_track(provider, tokens) -> Tuple[float, float]:
    CI = EAST_US_2_CI
    if provider == 'google-vertex':
        CI = CENTRAL_US_1_CI
    elif provider == 'groq':
        CI = DAMMAM_SAUDI_CI
    wh_token = WH_TOKEN_MAPPING[provider]
    energy_kwh = calculate_energy(wh_token, tokens)
    co2_kg = energy_kwh * CI
    return energy_kwh, co2_kg


