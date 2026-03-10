from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class UserAccountContext(BaseModel):

    customer_id: int
    name: str
    menu: str
    table_number: Optional[int] = None  # premium entreprise
    Reservation_time: Optional[datetime] =None
    Number_of_people_reserved: Optional[int] = None
    phone_number: str
    significant: Optional[str] = None
    

class InputGuardRailOutput(BaseModel):

    is_off_topic: bool
    reason: str


class HandoffData(BaseModel):

    to_agent_name: str
    issue_type: str
    issue_description: str
    reason: str