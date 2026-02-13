#!/usr/bin/python3
from app.models.base_model import BaseModel

class Review(BaseModel):
    def __init__(self, user_id, place_id, text):
        super().__init__()
        self.user_id = user_id
        self.place_id = place_id
        self.text = text

    def to_dict(self):
        base = super().to_dict()
        base.update({
            "user_id": self.user_id,
            "place_id": self.place_id,
            "text": self.text
        })
        return base


