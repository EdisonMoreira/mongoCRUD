from pydantic import BaseModel, ConfigDict
# from typing import Optional, Any
from uuid import UUID
from datetime import datetime

class User(BaseModel):

    # Permite campos extra além dos definidos abaixo 
    model_config = ConfigDict(extra='allow')  

    id: UUID
    name: str
    email: str
    released: datetime
    year: int
