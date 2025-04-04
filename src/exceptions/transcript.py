from .exception import BadRequest



class TranscriptNotFoundById(BadRequest):
    DETAIL ="Transcript not found by id"


class TransLateNotFound(BadRequest):
    DETAIL = "Translate not found by id"