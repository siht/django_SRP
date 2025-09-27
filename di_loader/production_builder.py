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
    components.registerAdapter(DjangoQuestionRepository, IQuestionRepository, ICreateQuestionExecutor)
    components.registerAdapter(DjangoChoiceRepository, IChoiceRepository, ICreateChoiceExecutor)
    components.registerAdapter(DjangoChoiceRepository, IChoiceRepository, IVoteExecutor)

