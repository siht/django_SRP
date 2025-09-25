# business_logic/interfaces.py
from typing import (
    Any,
    Protocol,
)

from . exceptions import (
    ChoiceNotFound,
    QuestionNotFound,
)
from .dtos import (
    ChoiceDTO,
    QuestionDTO,
)


class IQuestionRepository(Protocol):
    def create(self, question: QuestionDTO) -> QuestionDTO: ...
    def get_by_id(self, question_id: int) -> QuestionDTO | None | QuestionNotFound: ...
    def get_recent(self, limit: int=5) -> list[QuestionDTO]: ...


class IChoiceRepository(Protocol):
    """
    Define las operaciones mínimas para un repositorio que maneja 'Choice'.
    """
    
    def get_by_id(self, choice_id: int) -> ChoiceDTO | None | ChoiceNotFound:
        """Obtiene un DTO de un Choice por su ID."""
        ...
        
    def get_all(self) -> list[ChoiceDTO]:
        """Obtiene una lista de todos los DTOs de Choice."""
        ...

    def update_votes(self, choice_id: int) -> int:
        """Actualiza el número de votos para un Choice específico."""
        ...

    def create(self, choice: ChoiceDTO) -> ChoiceDTO:
        """
        Crea un nuevo Choice.
        Retorna el DTO del Choice creado.
        """
        ...

    def update(self, choice: ChoiceDTO) -> ChoiceDTO | None:
        """
        Actualiza un Choice existente.
        Retorna el DTO del Choice actualizado.
        """
        ...

    def delete(self, choice_id: int) -> None:
        """
        Elimina el Choice por su ID.
        """
        ...


class IServiceExecutor(Protocol):
    def execute(self) -> Any:
        pass
