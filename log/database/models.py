from datetime import datetime
from typing import List, Optional, Tuple, Union
from uuid import UUID, uuid4

from pydantic import BaseModel, Field

# @dataclass
# class TableMeta:
#     name: str
#     columns: List["TableColumnMeta"]

#     def _sql(self):
#         for each in self.columns:
#             each.name


# @dataclass
# class TableColumnMeta:
#     name: str
#     type: Any


class Message(BaseModel):
    content: str


class LogInfo(BaseModel):
    id: Optional[str] = Field(default_factory=lambda: str(uuid4()))
    date_time: Optional[Union[datetime, str]] | None = Field(
        default_factory=datetime.now
    )
    message: Message

    def sql_data(self):
        return tuple(
            str(each) for each in [self.id, self.date_time, self.message.content]
        )

    @classmethod
    def load_sql_data(cls, data: List[Tuple]):
        for each in data:
            yield LogInfo(
                id=each[0],
                date_time=datetime.strptime(each[1], "%Y-%m-%d %H:%M:%S.%f"),
                message=Message(
                    content=each[2],
                ),
            )
