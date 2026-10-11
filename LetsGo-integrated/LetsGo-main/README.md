# Campus & City Transit Tracking Web Application

A lightweight, real-time web application designed for educational campuses and city transit systems. The platform provides a streamlined dual-interface experience for users who need quick access to live transit information, route visibility, and schedule updates across both campus and urban environments.

## Overview

This project is built to help commuters, students, and transit stakeholders track vehicles in real time, monitor route movement, and improve overall transportation efficiency. It combines a responsive frontend interface with a backend API to support live data handling and route visibility.

## Key Features

- Real-time transit tracking for campus and city routes
- Dual-interface design optimized for users on different devices
- Easy access to route information and service status
- Lightweight architecture for quick deployment and use
- Simple setup for local development and testing

## Tech Stack

- Frontend: HTML, CSS, JavaScript
- Backend: Python, FastAPI
- Server: Uvicorn
- Local development: static frontend hosting or browser preview

## Project Structure

```bash
LetsGo/
├── backend/
│   ├── main.py            # FastAPI app, CORS, vehicle simulator, serves Frontend
│   ├── requirements.txt
│   └── app/               # models, schemas, routes, services
├── Frontend/
│   ├── index.html
│   ├── style.css
│   └── app.js             # Leaflet map, polls the REST API every 2s
└── README.md
```

## Getting Started

```bash
git clone https://github.com/ASH10022008/LetsGo.git
cd LetsGo/backend
pip install -r requirements.txt
uvicorn main:app --reload
```

Then open **http://localhost:8000/app/** (frontend + API from one server).
API docs: http://localhost:8000/docs

Alternatively, serve `Frontend/` with Live Server (port 5500); it will call the API at `http://localhost:8000/api`.

## How frontend and backend connect

- `GET /api/routes` is loaded once: draws route lines and stops.
- `GET /api/vehicles` is polled every 2 seconds: moves bus markers and updates the sidebar.
- A background task in `main.py` simulates vehicle movement along each route. To use real GPS data, send `PUT /api/vehicles/{id}` with `latitude` and `longitude` and remove the simulator.

## Usage

- Launch the backend server.
- Open the frontend application.
- View available routes and real-time movement details.
- Use the interface to monitor transit status and support campus or city travel planning.

## Team

This project is structured for collaborative development, with separate responsibilities for backend and frontend work.

## License

This project is currently distributed for educational and development purposes. Please review the repository for any additional licensing information before production deployment.

## Contact

For questions or collaboration inquiries, please contact the project maintainers through the repository owner or relevant team communication channel.
