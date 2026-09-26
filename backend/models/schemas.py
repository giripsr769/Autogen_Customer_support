from pydantic import BaseModel


class SupportRequest(BaseModel):
    query: str