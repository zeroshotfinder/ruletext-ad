from pydantic_ai.agent import AgentRunResult
from typing import Optional
from pydantic_ai import Agent
import httpx

from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.models.gemini import GeminiModel
from pydantic_ai.models.groq import GroqModel

from pydantic_ai.providers.azure import AzureProvider
from pydantic_ai.providers.google_vertex import GoogleVertexProvider
from pydantic_ai.providers.groq import GroqProvider

from pydantic_ai.messages import ModelRequest, ModelResponse
from pydantic_ai.messages import SystemPromptPart, UserPromptPart, TextPart

from box import Box
from billing import Billing
import env
import json
import dataclasses

class CustomHTTPClient(httpx.AsyncClient):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.last_billing: Optional[Billing] = None

    async def send(self, request: httpx.Request, **kwargs) -> httpx.Response:
        response = await super().send(request, **kwargs)
        body = response.json()
        self.last_billing = Billing(response.headers, body)
        return response


class AnomalyDetectionAgent(Agent):
    """."""

    def __init__(
        self,
        args
    ):

        self.llm_provider = args.model.provider
        self.llm_name = args.model.llm
        self._last_run: Optional[AgentRunResult] = None
        self._model_settings = {
            'temperature': args.model.temperature,
            'max_tokens': args.model.max_tokens,
            'seed':  args.model.seed,
        }
        
        if args.model.provider == 'openai':
            model = OpenAIModel(
                args.model.litellm,                
                provider=AzureProvider(
                    azure_endpoint=env.AZURE_ENDPOINT,
                    api_version=env.AZURE_API_VERSION,
                    api_key=env.AZURE_API_KEY,
                ),
            )
        elif args.model.provider == 'google-vertex':
            model = GeminiModel(
                args.model.litellm,
                provider=GoogleVertexProvider(
                    service_account_file=env.GOOGLE_APPLICATION_CREDENTIALS,
                    project_id = "cde-llm",
                    region = "us-central1",
                ),
            )
        elif args.model.provider == 'groq':
            model = GroqModel(
                args.model.litellm, provider=GroqProvider(api_key=env.GROQ_API_KEY)
            )

        super().__init__(model=model)

    async def run(self, user_prompt, message_history=[], output_type=None) -> AgentRunResult:
        retries = 5
        for _ in range(retries + 1):
            try:
                self._last_run = await super().run(
                    user_prompt=user_prompt,
                    message_history=message_history,
                    output_type=output_type,
                    model_settings=self._model_settings,
                )
                return self._last_run

            except Exception as e:
                self._model_settings['temperature'] += 0.1
                print("[agent.run] Connection fail, ...", e)
                continue
        raise ("[agent.run] Connection fail, ...")

    def build_history(self, system_prompt=None, agent_response=None, user_prompt=None):
        history_dicts = []
        if system_prompt:
            history_dicts.append({"role": "system", "content": system_prompt})
        if user_prompt:
            history_dicts.append({"role": "user", "content": agent_response})
        if agent_response:
            history_dicts.append({"role": "assistant", "content": agent_response})

        return  self.__convert_dict_to_message_history(history_dicts)

    def __convert_dict_to_message_history(self, hist_dicts):
        message_history = []
        for msg in hist_dicts:
            role = msg["role"]
            content = msg["content"]

            # Creating ModelRequest for user and system messages
            if role == "user":
                message_history.append(ModelRequest(parts=[UserPromptPart(content=content)], kind="request"))

            elif role == "system":
                message_history.append(ModelRequest(parts=[SystemPromptPart(content=content)], kind="request"))

            # Creating ModelResponse for assistant answers
            elif role == "assistant":
                message_history.append(ModelResponse(parts=[TextPart(content=content)], kind="response"))

        return message_history

    @property
    def usage(self):
        if self._last_run:
            if self.llm_provider == 'google-vertex':
                return Box(dataclasses.asdict(self._last_run.usage()))
            elif self.llm_provider == 'openai':
                return Box(dataclasses.asdict(self._last_run.usage()))
            elif self.llm_provider == 'groq':
                return Box(dataclasses.asdict(self._last_run.usage()))
        return  None

    @property
    def response_text(self):
        return self._last_run.data if self._last_run else None

    @property
    def model_info(self):
        return self._last_run.__dict__ if self._last_run else None

    @property
    def steps(self):
        return self._last_run.steps if self._last_run else []
