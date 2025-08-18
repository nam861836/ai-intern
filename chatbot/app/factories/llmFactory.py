# factories/llm_factory.py
from langchain_openai import ChatOpenAI
import os
from config.base_config import BaseConfiguration

config = BaseConfiguration()

class LLMFactory:
    @staticmethod
    def create():

        return ChatOpenAI(
            model=config.chat_model_config.model,
            temperature=config.chat_model_config.temperature
        )
