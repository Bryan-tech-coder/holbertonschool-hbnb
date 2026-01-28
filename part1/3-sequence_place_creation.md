# Sequence Diagram – Place Creation

## Description
Diagrama que muestra el flujo de interacción para la creación de un lugar.

```mermaid
sequenceDiagram
participant User
participant API
participant Facade
participant PlaceModel
participant Database

User->>API: POST /places
API->>Facade: create_place(data)
Facade->>PlaceModel: validate_owner()
PlaceModel->>Database: INSERT place
Database-->>PlaceModel: place_id
PlaceModel-->>Facade: Place created
Facade-->>API: success response
API-->>User: 201 Created
