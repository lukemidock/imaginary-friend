#convert sqlalchemy result to dict
def object_as_dict(obj):
    converted_obj = obj.__dict__
    converted_obj.pop('_sa_instance_state', None)
    return converted_obj

def list_objects_as_dict(listobj):
    data = []
    for obj in listobj:
        converted_obj = obj.__dict__
        converted_obj.pop('_sa_instance_state', None)
        data.append(converted_obj)
    return data