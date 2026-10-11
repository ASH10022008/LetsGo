from dataclasses import dataclass, field
from typing import List


@dataclass
class Stop:
    id: str
    name: str
    latitude: float
    longitude: float


@dataclass
class Route:
    id: str
    name: str
    color: str
    stops: List[Stop] = field(default_factory=list)


@dataclass
class Vehicle:
    id: str
    route_id: str
    name: str
    status: str
    current_stop_id: str | None = None
    latitude: float | None = None
    longitude: float | None = None
