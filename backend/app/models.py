
from pydantic import BaseModel
from datetime import datetime

class Users(BaseModel):
    email: str
    password: str
    full_name: str | None = None
    Address: str | None = None

class Bank(BaseModel):
    Bank_Name: str
    Bank_Account: str
    Bank_Routing: str
    Bank_Account_Type: str
    Bank_Account_Name: str
    Bank_Account_Number: str
    Bank_Account_Routing: str
    Bank_Account_Type: str
    Bank_Account_Name: str