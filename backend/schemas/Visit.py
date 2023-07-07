from pydantic import BaseModel, AnyHttpUrl


class Visit(BaseModel):
    end_user_id: str
    web_page_url: AnyHttpUrl
