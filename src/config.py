from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    app_name: str = "Ops Commander"
    environment: str = Field(default="development")

    github_token: str | None = None
    repo_full_name: str | None = None

    slack_webhook_url: str | None = None

    openai_api_key: str | None = None
    openai_model: str = "gpt-4.1-mini"

    aws_region: str = "us-east-1"
    aws_access_key_id: str | None = None
    aws_secret_access_key: str | None = None

    aws_devops_agent_enabled: bool = False

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()
