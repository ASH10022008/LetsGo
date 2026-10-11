from app.models import Route, Stop, Vehicle


CAMPUS_STOPS = [
    Stop(id="s1", name="Main Gate", latitude=12.9716, longitude=77.5946),
    Stop(id="s2", name="Library", latitude=12.9727, longitude=77.5957),
    Stop(id="s3", name="Student Center", latitude=12.9738, longitude=77.5968),
]

CITY_STOPS = [
    Stop(id="s4", name="Metro Station", latitude=12.9810, longitude=77.5820),
    Stop(id="s5", name="City Hall", latitude=12.9793, longitude=77.5841),
    Stop(id="s6", name="Market Square", latitude=12.9775, longitude=77.5862),
]


class TransitService:
    def __init__(self) -> None:
        self.routes = [
            Route(
                id="route-1",
                name="Campus Loop",
                color="#1d4ed8",
                stops=CAMPUS_STOPS,
            ),
            Route(
                id="route-2",
                name="City Connector",
                color="#f59e0b",
                stops=CITY_STOPS,
            ),
        ]

        self.vehicles = [
            Vehicle(
                id="bus-101",
                route_id="route-1",
                name="Campus Shuttle A",
                status="moving",
                current_stop_id="s2",
                latitude=12.9727,
                longitude=77.5957,
            ),
            Vehicle(
                id="bus-202",
                route_id="route-2",
                name="City Express",
                status="delayed",
                current_stop_id="s5",
                latitude=12.9793,
                longitude=77.5841,
            ),
        ]
        self._next_route_number = 3
        self._next_stop_number = 7
        self._next_vehicle_number = 103

    def _generate_id(self, prefix: str, current_number: int) -> str:
        generated = f"{prefix}-{current_number}"
        current_number += 1
        return generated, current_number

    def get_all_routes(self):
        return self.routes

    def get_route_by_id(self, route_id: str):
        for route in self.routes:
            if route.id == route_id:
                return route
        return None

    def create_route(self, route_data):
        route_id = route_data.id or f"route-{self._next_route_number}"
        self._next_route_number += 1

        stop_objects = []
        for stop_data in route_data.stops:
            stop_id = stop_data.id or f"stop-{self._next_stop_number}"
            self._next_stop_number += 1
            stop_objects.append(
                Stop(
                    id=stop_id,
                    name=stop_data.name,
                    latitude=stop_data.latitude,
                    longitude=stop_data.longitude,
                )
            )

        route = Route(
            id=route_id,
            name=route_data.name,
            color=route_data.color,
            stops=stop_objects,
        )
        self.routes.append(route)
        return route

    def update_route(self, route_id: str, route_data):
        route = self.get_route_by_id(route_id)
        if route is None:
            return None

        if route_data.name is not None:
            route.name = route_data.name
        if route_data.color is not None:
            route.color = route_data.color
        if route_data.stops is not None:
            route.stops = []
            for stop_data in route_data.stops:
                stop_id = stop_data.id or f"stop-{self._next_stop_number}"
                self._next_stop_number += 1
                route.stops.append(
                    Stop(
                        id=stop_id,
                        name=stop_data.name,
                        latitude=stop_data.latitude,
                        longitude=stop_data.longitude,
                    )
                )
        return route

    def delete_route(self, route_id: str):
        route = self.get_route_by_id(route_id)
        if route is None:
            return False

        self.vehicles = [vehicle for vehicle in self.vehicles if vehicle.route_id != route_id]
        self.routes = [existing_route for existing_route in self.routes if existing_route.id != route_id]
        return True

    def get_all_stops(self):
        stops = []
        for route in self.routes:
            stops.extend(route.stops)
        return stops

    def get_stop_by_id(self, stop_id: str):
        for stop in self.get_all_stops():
            if stop.id == stop_id:
                return stop
        return None

    def get_stops_for_route(self, route_id: str):
        route = self.get_route_by_id(route_id)
        if route is None:
            return None
        return route.stops

    def create_stop_for_route(self, route_id: str, stop_data):
        route = self.get_route_by_id(route_id)
        if route is None:
            return None

        stop_id = stop_data.id or f"stop-{self._next_stop_number}"
        self._next_stop_number += 1
        stop = Stop(
            id=stop_id,
            name=stop_data.name,
            latitude=stop_data.latitude,
            longitude=stop_data.longitude,
        )
        route.stops.append(stop)
        return stop

    def update_stop_for_route(self, route_id: str, stop_id: str, stop_data):
        route = self.get_route_by_id(route_id)
        if route is None:
            return None

        for stop in route.stops:
            if stop.id == stop_id:
                if stop_data.name is not None:
                    stop.name = stop_data.name
                if stop_data.latitude is not None:
                    stop.latitude = stop_data.latitude
                if stop_data.longitude is not None:
                    stop.longitude = stop_data.longitude
                return stop
        return None

    def delete_stop_from_route(self, route_id: str, stop_id: str):
        route = self.get_route_by_id(route_id)
        if route is None:
            return False

        original_length = len(route.stops)
        route.stops = [stop for stop in route.stops if stop.id != stop_id]
        for vehicle in self.vehicles:
            if vehicle.route_id == route_id and vehicle.current_stop_id == stop_id:
                vehicle.current_stop_id = None
        return len(route.stops) < original_length

    def get_all_vehicles(self):
        return self.vehicles

    def get_vehicle_by_id(self, vehicle_id: str):
        for vehicle in self.vehicles:
            if vehicle.id == vehicle_id:
                return vehicle
        return None

    def get_vehicles_for_route(self, route_id: str):
        return [vehicle for vehicle in self.vehicles if vehicle.route_id == route_id]

    def create_vehicle(self, vehicle_data):
        if vehicle_data.route_id and self.get_route_by_id(vehicle_data.route_id) is None:
            return None

        vehicle_id = vehicle_data.id or f"bus-{self._next_vehicle_number}"
        self._next_vehicle_number += 1
        vehicle = Vehicle(
            id=vehicle_id,
            route_id=vehicle_data.route_id,
            name=vehicle_data.name,
            status=vehicle_data.status,
            current_stop_id=vehicle_data.current_stop_id,
            latitude=vehicle_data.latitude,
            longitude=vehicle_data.longitude,
        )
        self.vehicles.append(vehicle)
        return vehicle

    def update_vehicle(self, vehicle_id: str, vehicle_data):
        vehicle = self.get_vehicle_by_id(vehicle_id)
        if vehicle is None:
            return None

        if vehicle_data.route_id is not None:
            route = self.get_route_by_id(vehicle_data.route_id)
            if route is None:
                return None
            vehicle.route_id = vehicle_data.route_id
        if vehicle_data.name is not None:
            vehicle.name = vehicle_data.name
        if vehicle_data.status is not None:
            vehicle.status = vehicle_data.status
        if vehicle_data.current_stop_id is not None:
            vehicle.current_stop_id = vehicle_data.current_stop_id
        if vehicle_data.latitude is not None:
            vehicle.latitude = vehicle_data.latitude
        if vehicle_data.longitude is not None:
            vehicle.longitude = vehicle_data.longitude
        return vehicle

    def delete_vehicle(self, vehicle_id: str):
        vehicle = self.get_vehicle_by_id(vehicle_id)
        if vehicle is None:
            return False
        self.vehicles = [existing_vehicle for existing_vehicle in self.vehicles if existing_vehicle.id != vehicle_id]
        return True

    def get_status(self):
        return {
            "status": "healthy",
            "services": ["routes", "vehicles", "tracking"],
        }


transit_service = TransitService()
