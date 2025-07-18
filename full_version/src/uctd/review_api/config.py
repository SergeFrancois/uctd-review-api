from envyaml import EnvYAML
from pydantic import AnyUrl, BaseModel, ConfigDict, Field
from . import constants


class BaseConfig(BaseModel):
    model_config = ConfigDict(populate_by_name=True)


class DbConfig(BaseConfig):
    echo: bool = False
    url: AnyUrl


class Config(BaseConfig):
    db: DbConfig


def load_config_from_yaml(path):
    env = EnvYAML(path, flatten=False)
    return Config.model_validate(env.export())


config = load_config_from_yaml(constants.CONFIG_PATH)