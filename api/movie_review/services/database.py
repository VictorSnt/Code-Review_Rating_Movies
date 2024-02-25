from ninja.errors import HttpError

class DataBase:
    def __init__(self, model, query_key) -> None:
        self.model = model
        self.query_key = query_key
    
    def get_obj(self):
        key = self.query_key
        model = self.model
        obj = model.objects.filter(key=key).first()
        if not obj:
            raise HttpError(404, "Objeto não encontrado")
        return obj
    
    def update_obj(self, obj, update_data: dict):
        is_updated = False
        for field, value in update_data.items():
            if value:
                is_updated = True
                setattr(obj, field, value)
        if not is_updated:
            raise HttpError(400, "Nenhum campo valido foi preenchido") 
        else:
            obj.save()
            return obj