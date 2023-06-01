import os
import secrets
from typing import Any, Dict, List, Optional, Union

from pydantic import BaseSettings, PostgresDsn, validator

# --------------------------------
#
# --------------------------------
#
class Settings(BaseSettings):
    """Class for handling the environment variable settings.

    Approach taken from https://fastapi.tiangolo.com/advanced/settings/
    """

    # --------------------------------
    # env variables
    # --------------------------------

    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "test-fastAPI"
    PROJECT_ID: str = "test-platform-lab"
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 60 minutes * 24 hours * 8 days = 8 days
    SERVER_NAME: str = ""
    SERVER_HOST: str = "http://localhost"
    BACKEND_CORS_ORIGINS: str = '["http://localhost:4200", "http://dev.test-main:3000"]'
    POSTGRES_SERVER: str = ""
    POSTGRES_USER: str = ""
    POSTGRES_PASSWORD: str = ""
    POSTGRES_DB: str = ""
    SESSION_DATABASE_URI: Optional[PostgresDsn]

    # --------------------------------
    # field validators
    # --------------------------------
    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    @validator("SESSION_DATABASE_URI")
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgresql",
            user=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            host=values.get("POSTGRES_SERVER"),
            path=f"/{values.get('POSTGRES_DB') or ''}",
        )

    # --------------------------------
    # Pydantic model config: https://pydantic-docs.helpmanual.io/usage/model_config/
    # --------------------------------

    class Config:
        case_sensitive = True

        # check for local run
        if os.getenv("POSTGRES_SERVER") is None:
            env_file = ".env"


settings = Settings()
