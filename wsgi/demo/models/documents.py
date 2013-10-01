from datetime import datetime
from pymongo.objectid import ObjectId
from demo import db, redis_cli

class Todo(db.Document):

    def clean4_dump(self):
        """
        Removes the ObjectID types from an object 
        before returning
        """
        response = dict(self._field_values)
        for field in self._fields:
            try:
                field_value = self.__getattribute__(field)
                if isinstance(field_value, 
                        ObjectId):
                    response[field] = str(self.__getattribute__(field))
                elif isinstance( field_value, list):
                    field_value = [ value.clean4_dump() for 
                            value in field_value ]
                    response[field] = field_value
                elif isinstance( field_value,
                        dict):
                    field_value = dict( [ (str(key), value.clean4_dump()) for key, value in field_value.items() ])
                    response[field] = field_value
            except AttributeError:
                continue
        return response

    mongo_id = db.ObjectIdField()
    title = db.StringField()
    completed = db.BoolField()
    order = db.AnythingField()
