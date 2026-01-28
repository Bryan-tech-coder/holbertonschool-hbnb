
# Business Logic Layer – Class Diagram

## Description
Este diagrama muestra las entidades principales del negocio y sus relaciones.

```mermaid
classDiagram

class BaseEntity {
    +UUID id
    +datetime created_at
    +datetime updated_at
}

class User {
    +string first_name
    +string last_name
    +string email
    +string password
    +boolean is_admin
    +register()
    +update_profile()
    +delete()
}

class Place {
    +string title
    +string description
    +float price
    +float latitude
    +float longitude
    +create()
    +update()
    +delete()
}

class Review {
    +int rating
    +string comment
    +create()
    +update()
    +delete()
}

class Amenity {
    +string name
    +string description
    +create()
    +update()
    +delete()
}

BaseEntity <|-- User
BaseEntity <|-- Place
BaseEntity <|-- Review
BaseEntity <|-- Amenity

User "1" --> "0..*" Place : owns
User "1" --> "0..*" Review : writes
Place "1" --> "0..*" Review : receives
Place "0..*" -- "0..*" Amenity : has
