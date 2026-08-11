from app import db


class BaseRepository:
    """
    Generic Base Repository.
    Other repositories inherit from this class.
    """

    def __init__(self, model):
        self.model = model

    def create(self, obj):
        db.session.add(obj)
        db.session.commit()
        return obj

    def get_all(self):
        return self.model.query.all()

    def get_by_id(self, obj_id):
        return self.model.query.get(obj_id)

    def update(self):
        db.session.commit()

    def delete(self, obj):
        db.session.delete(obj)
        db.session.commit()