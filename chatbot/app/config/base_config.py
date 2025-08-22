"""Define the configurable parameters for the agent."""

from __future__ import annotations

from typing import Annotated, Dict, Literal, Optional, Type, TypeVar, Union, cast

from dotenv import load_dotenv
from langchain_core.runnables import RunnableConfig, ensure_config
from langchain_core.utils import from_env, secret_from_env
from pydantic import BaseModel, Field, SecretStr, model_validator
from typing_extensions import Self

from utils.utils import get_value_from_dict

from .config_loader import CONFIG

load_dotenv(override=True)

class OpenAIConfig(BaseModel):
    api_key: SecretStr = Field(default_factory=secret_from_env("OPENAI_API_KEY"))
    model: str = Field(default_factory=from_env("OPENAI_MODEL"))
    embed_model: str = Field(default_factory=from_env("OPENAI_EMBED_MODEL"))
    temperature: float = Field(default_factory=from_env("TEMPERATURE"))
    
class TavilyConfig(BaseModel):
    api_key: SecretStr = Field(default_factory=secret_from_env("TAVILY_API_KEY"))

class MongoDBConfig(BaseModel):
    uri: str = Field(default_factory=from_env("MONGODB_URI"))
    
class RedisConfig(BaseModel):
    host: str = Field(default_factory=from_env("REDIS_HOST"))
    password: SecretStr = Field(default_factory=secret_from_env("REDIS_PASSWORD"))

class BaseConfiguration(BaseModel):
    chunk_size: int = Field(
        default_factory=lambda: get_value_from_dict("chunk_config.chunk_size", CONFIG, default=1000)()
    )
    chunk_overlap: int = Field(
        default_factory=lambda: get_value_from_dict("chunk_config.chunk_overlap", CONFIG, default=200)()
    )
    pdf_path: str = Field(default_factory=lambda: get_value_from_dict("path.pdf", CONFIG, default="./data/policy.pdf")())
    db_path: str = Field(default_factory=lambda: get_value_from_dict("path.db", CONFIG, default="./data/user_ticket.db")())

    chat_model_config: OpenAIConfig = Field(default_factory=OpenAIConfig)
    embedding_model_config: OpenAIConfig = Field(default_factory=OpenAIConfig)
    tavily_config: TavilyConfig = Field(default_factory=TavilyConfig)
    mongodb_config: MongoDBConfig = Field(default_factory=MongoDBConfig)
    redis_config: RedisConfig = Field(default_factory=RedisConfig)
