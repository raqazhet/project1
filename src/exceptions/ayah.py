from .exception import BadRequest

class AyahNotFound(BadRequest):
    DETAIL = "Ayah not found by id"