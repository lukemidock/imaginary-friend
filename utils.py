from flask_sqlalchemy import inspect

#convert sqlalchemy result to dict
def object_as_dict(obj):
    converted_obj = obj.__dict__
    converted_obj.pop('_sa_instance_state', None)
    return obj.__dict__