#!/usr/bin/python3
"""
In-memory repository for HBnB
"""

import uuid


class InMemoryRepository:
    def __init__(self):
        self._storage = {}

    def add(self, obj):
        """Add an object to storage"""
        self._storage[obj.id] = obj

    def get(self, obj_id):
        """Retrieve object by ID"""
        return self._storage.get(obj_id)

    def get_all(self):
        """Return all objects"""
        return list(self._storage.values())

    def update(self, obj_id, data):
        """Update an object"""
        obj = self.get(obj_id)
        if not obj:
            return None
        for key, value in data.items():
            if hasattr(obj, key):
                setattr(obj, key, value)
        return obj

    def delete(self, obj_id):
        """Delete object"""
        return self._storage.pop(obj_id, None)
