# Sequence Diagram – Review Submission

## Description
Diagrama que muestra el flujo de interacción para enviar una reseña de un lugar.

```mermaid
sequenceDiagram
participant User
participant API
participant Facade
participant ReviewModel
participant Database

User->>API: POST /reviews
API->>Facade: create_review(data)
Facade->>ReviewModel: validate_place_user()
ReviewModel->>Database: INSERT review
Database-->>ReviewModel: review_id
ReviewModel-->>Facade: Review created
Facade-->>API: success response
API-->>User: 201 Created
