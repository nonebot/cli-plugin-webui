from typing import List, Optional

from pydantic import BaseModel


class TestResult(BaseModel):
    validation: bool
    load: bool
    metadata: bool


class TestInput(BaseModel):
    config: str


class TestMetadata(BaseModel):
    name: str
    description: str
    usage: str
    type: str
    homepage: str
    supported_adapters: Optional[List[str]]


class TestOutput(BaseModel):
    validation: str
    load: str
    metadata: TestMetadata


class RegistryResult(BaseModel):
    time: str
    version: str
    results: TestResult
    inputs: TestInput
    outputs: TestOutput
