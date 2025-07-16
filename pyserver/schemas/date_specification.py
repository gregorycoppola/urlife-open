from pydantic import BaseModel
from typing import List

class DateSpecification(BaseModel):
    type_name: str
    has_due_date: bool
    has_due_time: bool
    has_start_date: bool
    has_start_time: bool
    has_end_date: bool
    has_end_time: bool

class AllDateSpecifications(BaseModel):
    specifications: List[DateSpecification]
