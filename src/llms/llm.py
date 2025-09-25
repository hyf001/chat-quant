import os
from pickle import NONE
from langchain_openai import ChatOpenAI
from openai import api_key
from src.config.agents import LLMType
from langchain_core.language_models import BaseChatModel
from src.config.loader import load_yaml_config
from pathlib import Path
from src.config import loader


_llm_cache : dict[LLMType,BaseChatModel] = {}



def get_llm_by_type(
    llm_type: LLMType,
) -> BaseChatModel:
    """
    Get LLM instance by type. Returns cached instance if available.
    """
    if llm_type in _llm_cache:
        return _llm_cache[llm_type]
    MODEL_NAME = os.getenv('MODEL_NAME')
    if llm_type == "moonshot":
        llm = ChatOpenAI(model= MODEL_NAME if MODEL_NAME else "kimi-k2-250905",max_tokens=32768)
        _llm_cache[llm_type] = llm
    else:
        llm = ChatOpenAI(model= MODEL_NAME if MODEL_NAME else "kimi-k2-250905",max_tokens=102400)
        _llm_cache[llm_type] = llm
    return llm