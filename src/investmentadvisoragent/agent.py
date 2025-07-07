import abc
import os

from dotenv import load_dotenv
from google.genai import Client, types

from investmentadvisoragent.data.user_info import UserInfo


class Agent(abc.ABC):
    """An implementation of an agent that is meant to make life a bit easier without relying on some of the complexities of libraries like langchain."""

    def __init__(self, user_info: UserInfo, agent_name: str, agent_model: str) -> None:
        """Initialize the Agent."""
        load_dotenv()
        self._client = Client(
            api_key=os.environ["AI_STUDIO_API_KEY"],
        )
        self._agent_name = agent_name
        self._agent_model = agent_model
        self._user_info = user_info
        self._tools = {}
        # Will be overwritten by other agents - not the best way to do this.
        self._prompt = ""

    @property
    @abc.abstractmethod
    def tools(self) -> list[types.Tool]:
        """Return the tools that the agent has access to."""
        raise NotImplementedError

    def chat(self, prompt: str) -> str:
        """Chat with the agent."""
        contents = [
            types.Content(
                parts=[
                    types.Part.from_text(
                        text=self._prompt + f"\nThe users prompt is {prompt}"
                    )
                ],
                role="user",
            )
        ]
        while True:
            response = self._client.models.generate_content(
                contents=contents,
                model=self._agent_model,
                config=types.GenerateContentConfig(tools=self.tools),
            )
            if not response.function_calls:
                print(f"[{self._agent_name}]: {response.text}")
                return response.text
            contents = contents + [
                response.candidates[0].content
            ]  # Update the content history.
            for call in response.function_calls:
                print(f"Calling {call.name} with args {call.args}...")
                res = self._tools[call.name](**call.args)
                print(f"Response is {res}")
                if not isinstance(res, dict):
                    res = {"response": res}
                contents.append(
                    types.Part.from_function_response(name=call.name, response=res)
                )
