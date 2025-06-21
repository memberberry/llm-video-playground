from typing import List, Dict, Literal, Optional, Any
from typing_extensions import TypedDict
from pydantic import BaseModel
from google.genai.types import GenerateContentConfigOrDict
from google.genai.types import Type

class GeminiFileRequest(BaseModel):
    model: str
    prompt: str
    files: List[str]

class PropertyDefinition(TypedDict):
    # 'STRING', 'INTEGER', 'NUMBER', 'BOOLEAN', 'ARRAY', 'OBJECT'
    type: Literal[Type.STRING, Type.INTEGER, Type.NUMBER, Type.BOOLEAN, Type.ARRAY, Type.OBJECT]
    description: str

PropertiesDict = Dict[str, PropertyDefinition]

class ResponseSchemaDict(TypedDict):
    required: List[str]
    properties: PropertiesDict
    type: Literal["OBJECT"]


class GeminiStructRequest(BaseModel):
    # schema={
    #         'required': [
    #             'name',
    #             'population',
    #             'capital',
    #             'continent',
    #             'gdp',
    #             'official_language',
    #             'total_area_sq_mi',
    #         ],
    #         'properties': {
    #             'name': {'type': 'STRING'},
    #             'population': {'type': 'INTEGER'},
    #             'capital': {'type': 'STRING'},
    #             'continent': {'type': 'STRING'},
    #             'gdp': {'type': 'INTEGER'},
    #             'official_language': {'type': 'STRING'},
    #             'total_area_sq_mi': {'type': 'INTEGER'},
    #         },
    #         'type': 'OBJECT',
    #     },
    model: str
    prompt: str
    files: List[str]
    response_schema: ResponseSchemaDict 

class History(BaseModel):
    id: int
    prompt: str
    model: str
    output: Optional[str]
    structured_output: Optional[Dict[str, Any]]
    created_at: str
    videos: List[str]
