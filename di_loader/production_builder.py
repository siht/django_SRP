from twisted.python import components

from business_logic.interfaces import (
    IChoiceRepository,
    ICreateChoiceExecutor,
    ICreateQuestionExecutor,
    IQuestionRepository,
    IVoteExecutor,
)

from polls.question_service import DjangoQuestionRepository
from polls.choice_service import DjangoChoiceRepository

def main():
    components.registerAdapter(DjangoQuestionRepository, ICreateQuestionExecutor, IQuestionRepository)
    components.registerAdapter(DjangoChoiceRepository, ICreateChoiceExecutor, IChoiceRepository)
    components.registerAdapter(DjangoChoiceRepository, IVoteExecutor, IChoiceRepository)

