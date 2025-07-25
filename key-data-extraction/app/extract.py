import os
from langchain_openai import ChatOpenAI
from typing import Optional, List
from pydantic import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import LLMChain

from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())
openai_api_key = os.environ["OPENAI_API_KEY"]
model = os.environ["OPENAI_MODEL"]
temperature = os.environ["TEMPERATURE"]

llm = ChatOpenAI(model=model, temperature=temperature)

class Person(BaseModel):
    first_name: Optional[str] = Field(
        default=None, description="The first name of the person if known"
    )
    last_name: Optional[str] = Field(
        default=None, description="The last name of the person if known"
    )
    country: Optional[str] = Field(
        default=None, description="The country of the person if known"
    )
class Data(BaseModel):
    people: List[Person] = Field(description="The list of people extracted from the text")

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are an expert extraction algorithm. "
            "Only extract relevant information from the text. "
            "If you do not know the value of an attribute asked to extract, "
            "return null for the attribute's value.",
        ),
        ("human", "{text}"),
    ]
)

chain = prompt | llm.with_structured_output(schema=Data)
comment = "Dr. Arisara Somsuk, from Thailand, recently collaborated on a research project with Professor Liam O'Connell, who hails from Ireland. Their joint efforts have led to significant advancements in the field."
print(chain.invoke({"text": comment}))

