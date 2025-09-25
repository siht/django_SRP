# business_logic/dtos.py
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from .exceptions import ChoiceDataError


@dataclass
class QuestionDTO:
    """Entidad de dominio - solo datos, sin lógica, excepto validaciones"""
    question_text: str
    id: Optional[int] = None
    pub_date: Optional[datetime] = None


@dataclass
class ChoiceDTO:
    """Entidad de dominio - solo datos, sin lógica, excepto validaciones"""
    text: str
    question_id: Optional[int] = None
    id: Optional[int] = None
    votes: Optional[int] = None

    def __post_init__(self):
        no_ingresaron_votos_iniciales = self.votes is None
        if no_ingresaron_votos_iniciales:
            self.votes = 0
        es_un_dto_para_creacion = not self.id and not self.question_id
        if es_un_dto_para_creacion:
            raise ChoiceDataError('es necesario el campo question_id para la creacion de un Choice')
