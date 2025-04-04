from .exception import BadRequest


class HadithNotFoundById(BadRequest):
    DETAIL = "Hadith not found by id"


class FileNotFoundById(BadRequest):
    DETAIL = "File not found by id"