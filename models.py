from pydantic import BaseModel
from typing import Optional

class Email(BaseModel):
    subject: str
    body: str
    label: str

class Action(BaseModel):
    action: str

class StepResponse(BaseModel):
    observation: Email
    reward: float
    done: bool
    info: dict