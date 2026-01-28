# High-Level Package Diagram – HBnB

## Description
Este diagrama muestra la arquitectura de 3 capas con el patrón Facade para HBnB.

```mermaid
classDiagram

class PresentationLayer {
    <<Layer>>
    API
    Services
}

class BusinessLogicLayer {
    <<Facade>>
    HBnBFacade
    User
    Place
    Review
    Amenity
}

class PersistenceLayer {
    <<Layer>>
    Repository
    Database
}

PresentationLayer --> BusinessLogicLayer : uses Facade
BusinessLogicLayer --> PersistenceLayer : CRUD operations
