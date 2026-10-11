from fastapi import APIRouter, HTTPException, status

from app.schemas import (
    RouteCreateSchema,
    RouteSchema,
    RouteUpdateSchema,
    ServiceStatusSchema,
    StopCreateSchema,
    StopSchema,
    StopUpdateSchema,
    VehicleCreateSchema,
    VehicleSchema,
    VehicleUpdateSchema,
)
from app.services import transit_service

router = APIRouter(tags=["Transit"])


@router.get("/health")
def health_check():
    return {"status": "ok"}


@router.get("/status", response_model=ServiceStatusSchema)
def service_status():
    return transit_service.get_status()


@router.get("/routes", response_model=list[RouteSchema])
def get_routes():
    return transit_service.get_all_routes()


@router.post("/routes", response_model=RouteSchema, status_code=status.HTTP_201_CREATED)
def create_route(route: RouteCreateSchema):
    created_route = transit_service.create_route(route)
    return created_route


@router.get("/routes/{route_id}", response_model=RouteSchema)
def get_route(route_id: str):
    route = transit_service.get_route_by_id(route_id)
    if route is None:
        raise HTTPException(status_code=404, detail="Route not found")
    return route


@router.put("/routes/{route_id}", response_model=RouteSchema)
def update_route(route_id: str, route: RouteUpdateSchema):
    updated_route = transit_service.update_route(route_id, route)
    if updated_route is None:
        raise HTTPException(status_code=404, detail="Route not found")
    return updated_route


@router.delete("/routes/{route_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_route(route_id: str):
    deleted = transit_service.delete_route(route_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Route not found")
    return None


@router.get("/stops", response_model=list[StopSchema])
def get_stops():
    return transit_service.get_all_stops()


@router.get("/stops/{stop_id}", response_model=StopSchema)
def get_stop(stop_id: str):
    stop = transit_service.get_stop_by_id(stop_id)
    if stop is None:
        raise HTTPException(status_code=404, detail="Stop not found")
    return stop


@router.get("/routes/{route_id}/stops", response_model=list[StopSchema])
def get_route_stops(route_id: str):
    route = transit_service.get_route_by_id(route_id)
    if route is None:
        raise HTTPException(status_code=404, detail="Route not found")
    return transit_service.get_stops_for_route(route_id)


@router.post("/routes/{route_id}/stops", response_model=StopSchema, status_code=status.HTTP_201_CREATED)
def create_route_stop(route_id: str, stop: StopCreateSchema):
    route = transit_service.get_route_by_id(route_id)
    if route is None:
        raise HTTPException(status_code=404, detail="Route not found")
    created_stop = transit_service.create_stop_for_route(route_id, stop)
    return created_stop


@router.put("/routes/{route_id}/stops/{stop_id}", response_model=StopSchema)
def update_route_stop(route_id: str, stop_id: str, stop: StopUpdateSchema):
    route = transit_service.get_route_by_id(route_id)
    if route is None:
        raise HTTPException(status_code=404, detail="Route not found")

    updated_stop = transit_service.update_stop_for_route(route_id, stop_id, stop)
    if updated_stop is None:
        raise HTTPException(status_code=404, detail="Stop not found")
    return updated_stop


@router.delete("/routes/{route_id}/stops/{stop_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_route_stop(route_id: str, stop_id: str):
    route = transit_service.get_route_by_id(route_id)
    if route is None:
        raise HTTPException(status_code=404, detail="Route not found")

    deleted = transit_service.delete_stop_from_route(route_id, stop_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Stop not found")
    return None


@router.get("/vehicles", response_model=list[VehicleSchema])
def get_vehicles():
    return transit_service.get_all_vehicles()


@router.post("/vehicles", response_model=VehicleSchema, status_code=status.HTTP_201_CREATED)
def create_vehicle(vehicle: VehicleCreateSchema):
    created_vehicle = transit_service.create_vehicle(vehicle)
    if created_vehicle is None:
        raise HTTPException(status_code=404, detail="Route not found")
    return created_vehicle


@router.get("/vehicles/{vehicle_id}", response_model=VehicleSchema)
def get_vehicle(vehicle_id: str):
    vehicle = transit_service.get_vehicle_by_id(vehicle_id)
    if vehicle is None:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    return vehicle


@router.put("/vehicles/{vehicle_id}", response_model=VehicleSchema)
def update_vehicle(vehicle_id: str, vehicle: VehicleUpdateSchema):
    updated_vehicle = transit_service.update_vehicle(vehicle_id, vehicle)
    if updated_vehicle is None:
        raise HTTPException(status_code=404, detail="Vehicle not found or route not found")
    return updated_vehicle


@router.delete("/vehicles/{vehicle_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_vehicle(vehicle_id: str):
    deleted = transit_service.delete_vehicle(vehicle_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    return None


@router.get("/routes/{route_id}/vehicles", response_model=list[VehicleSchema])
def get_route_vehicles(route_id: str):
    route = transit_service.get_route_by_id(route_id)
    if route is None:
        raise HTTPException(status_code=404, detail="Route not found")
    return transit_service.get_vehicles_for_route(route_id)
