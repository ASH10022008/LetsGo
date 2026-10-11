from typing import Optional

from pydantic import BaseModel, Field


class StopSchema(BaseModel):
    id: str
    name: str
    latitude: float
    longitude: float


class StopCreateSchema(BaseModel):
    id: Optional[str] = None
    name: str
    latitude: float
    longitude: float


class StopUpdateSchema(BaseModel):
    name: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None


class RouteSchema(BaseModel):
    id: str
    name: str
    color: str
    stops: list[StopSchema] = Field(default_factory=list)


class RouteCreateSchema(BaseModel):
    id: Optional[str] = None
    name: str
    color: str = "#2563eb"
    stops: list[StopCreateSchema] = Field(default_factory=list)


class RouteUpdateSchema(BaseModel):
    name: Optional[str] = None
    color: Optional[str] = None
    stops: Optional[list[StopCreateSchema]] = None


class VehicleSchema(BaseModel):
    id: str
    route_id: str
    name: str
    status: str
    current_stop_id: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None


class VehicleCreateSchema(BaseModel):
    id: Optional[str] = None
    route_id: str
    name: str
    status: str = "idle"
    current_stop_id: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None


class VehicleUpdateSchema(BaseModel):
    route_id: Optional[str] = None
    name: Optional[str] = None
    status: Optional[str] = None
    current_stop_id: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None


class ServiceStatusSchema(BaseModel):
    status: str
    services: list[str]
