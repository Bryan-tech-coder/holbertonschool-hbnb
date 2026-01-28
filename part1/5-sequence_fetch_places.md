# Sequence Diagram – Fetching a List of Places

## Description
Diagrama que muestra el flujo de interacción para obtener la lista de lugares.

```mermaid
sequenceDiagram
participant User
participant API
participant Facade
participant PlaceModel
participant Database

User->>API: GET /places
API->>Facade: get_places(filters)
Facade->>PlaceModel: fetch_places(filters)
PlaceModel->>Database: SELECT places
Database-->>PlaceModel: places list
PlaceModel-->>Facade: formatted places
Facade-->>API: places data
API-->>User: 200 OK
