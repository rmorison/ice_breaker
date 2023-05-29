from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field


class PersonIntel(BaseModel):
    summary: str = Field(description="Summary of the person")
    facts: list[str] = Field(
        description="Interesting facts about the person"
    )
    topics_of_interest: list[str] = Field(
        description="Topics that may interest the person"
    )
    ice_breakers: list[str] = Field(
        description="Create ice breakers to open a conversation with the person"
    )

    def to_dict(self):
        return self.dict()


person_intel_parser = PydanticOutputParser(pydantic_object=PersonIntel)
