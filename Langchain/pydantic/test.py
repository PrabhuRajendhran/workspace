from datetime import datetime
from typing import Tuple

from pydantic import BaseModel


class Delivery(BaseModel):
    timestamp: datetime
    dimensions: list[int, int]

class Order(BaseModel):
    timestamp: datetime
    items: list[str, str]


m = Delivery(timestamp='2020-01-02T03:04:05Z', dimensions= (10, 10))
print(repr(m.timestamp))
#> datetime.datetime(2020, 1, 2, 3, 4, 5, tzinfo=TzInfo(UTC))
print(m.dimensions)
#> (10, 20)

a = Order(timestamp='2020-01-02T03:04:05Z', items = ('pulav', 'gogi', 'ddd', 'sss'))
print(repr(a.timestamp))
#> datetime.datetime(2020, 1, 2, 3, 4, 5, tzinfo=TzInfo(UTC))
print(a.items)
#> (10, 20)
