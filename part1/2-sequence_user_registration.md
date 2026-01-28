# Sequence Diagram – User Registration

## Description
Diagrama que muestra el flujo de interacción para el registro de un nuevo usuario.

```mermaid
sequenceDiagram
participant User
participant API
participant Facade
participant UserModel
participant Database

User->>API: POST /users
API->>Facade: register_user(data)
Facade->>UserModel: create_user(data)
UserModel->>Database: INSERT user
Database-->>UserModel: user_id
UserModel-->>Facade: User created
Facade-->>API: success response
API-->>User: 201 Created
