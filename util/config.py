
import os
import yaml
from typing import Any
import logging

class Config:
    """配置类"""
    
    def __init__(self,config_path: str = 'config/config.yaml'):
        self.config_path = config_path
        self.config = self._load_config()
    
    def _load_config(self) -> dict[str,Any]:
        config = {}
        #加载配置文件
        if os.path.exists(self.config_path):
            with open(self.config_path,'r',encoding='utf-8') as f:
                config = yaml.safe_load(f)
                logging.info(f"加载配置文件{self.config_path}")
        return config

    def get(self,key: str,default: Any = None) -> Any:
        keys = key.split('.')
        value = self.config
        for k in keys:
            if isinstance(value,dict) and k in value:
                value = value[k]
            else:
                return default
        return value
    
config = Config()