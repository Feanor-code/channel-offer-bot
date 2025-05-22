from typing import Any

from aiogram import types
from aiogram import filters
from pydantic import BaseModel


class SmartFilter(BaseModel, filters.BaseFilter):
    prefix: str = ""

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)

    async def __call__(self, query: types.CallbackQuery) -> None | dict[str, Any]:
        if not query.data or not query.data.startswith(self.prefix):
            return
        
        raw_data = query.data[len(self.prefix):]
        parts = raw_data.split(":")
        field_names = list(self.__class__.model_fields.keys())

        if len(parts) != len(field_names):
            return
        
        try:
            data = dict(zip(field_names, parts))
            classed = self.__class__(**data)
        except Exception:
            return
        
        return classed.model_dump()

    def pack(self) -> str:
        return ":".join(map(str, self.model_dump().values()))
