classDiagram
    %% Base Model
    class BaseModel {
        +id: str
        +created_at: datetime
        +updated_at: datetime
        +save()
        +to_dict()
    }

    %% User
    class User {
        +first_name: str
        +last_name: str
        +email: str
        +to_dict()
    }

    %% Place
    class Place {
        +name: str
        +description: str
        +number_rooms: int
        +number_bathrooms: int
        +max_guest: int
        +price_by_night: float
        +latitude: float
        +longitude: float
        +owner_id: str
        +amenity_ids: list
        +review_ids: list
        +to_dict()
    }

    %% Amenity
    class Amenity {
        +name: str
        +to_dict()
    }

    %% Review
    class Review {
        +user_id: str
        +place_id: str
        +text: str
        +to_dict()
    }

    %% Facade
    class HBnBFacade {
        +create_user(data)
        +get_user(user_id)
        +get_all_users()
        +update_user(user_id, data)
        +create_place(data)
        +get_place(place_id)
        +get_all_places()
        +update_place(place_id, data)
        +create_amenity(data)
        +get_amenity(amenity_id)
        +get_all_amenities()
        +update_amenity(amenity_id, data)
        +create_review(data)
        +get_review(review_id)
        +get_all_reviews()
        +update_review(review_id, data)
        +delete_review(review_id)
    }

    %% Herencia
    BaseModel <|-- User
    BaseModel <|-- Place
    BaseModel <|-- Amenity
    BaseModel <|-- Review

    %% Relaciones
    User "1" --> "*" Place : owns
    Place "1" --> "*" Review : has
    Place "*" --> "*" Amenity : includes
    Review "*" --> "1" User : written_by
    Review "*" --> "1" Place : belongs_to
