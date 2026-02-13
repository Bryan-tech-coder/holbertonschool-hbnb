#!/usr/bin/python3
class InMemoryRepository:
    def __init__(self):
        self.data = {}

    def add(self, obj):
        self.data[obj.id] = obj

    def get(self, obj_id):
        return self.data.get(obj_id)

    def get_all(self):
        return list(self.data.values())

    def update(self, obj_id, new_data):
        obj = self.get(obj_id)
        if not obj:
            return None
        for key, value in new_data.items():
            if hasattr(obj, key):
                setattr(obj, key, value)
        obj.save()
        return obj

    def delete(self, obj_id):
        return self.data.pop(obj_id, None)
