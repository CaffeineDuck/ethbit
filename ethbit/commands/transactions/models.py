import typing as t
from pydantic import BaseModel, validator
from pydantic.fields import Field


class Transaction(BaseModel):
    hash_: t.Any = Field(alias="hash")
    nonce: int
    blockHash: t.Any
    blockNumber: int
    transactionIndex: int
    by: t.Any = Field(alias="from")
    to: t.Any
    value: int
    gas: int
    gasPrice: int

    @validator("to", "by", "blockHash", "hash_")
    def hash_validator(cls, v):
        if hasattr(v, "hex"):
            return v.hex()
        return str(v)

    @validator("gasPrice", "value")
    def convert_to_ether(cls, v):
        return int(v) / 10**18

    class Config:
        check_fields = False
        ignore_extra = True
