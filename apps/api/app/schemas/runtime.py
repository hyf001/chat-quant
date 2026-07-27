from pydantic import BaseModel


class RuntimeHealthResponse(BaseModel):
    status: str
    python_version: str
    packages: dict[str, str]
    project_home_writable: bool
