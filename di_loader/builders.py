# di_loader/builders.py

from twisted.python import components

from business_logic.interfaces import (
    IChoiceRepository,
    ICreateChoiceExecutor,
    ICreateQuestionExecutor,
    IQuestionRepository,
    IVoteExecutor,
)
from business_logic.use_cases import (
    CreateChoice,
    CreateQuestion,
    Vote,
)
from business_logic.misc.helper_interfaces import (
    IChoiceCreatorIOFrameworkAdapter,
    IQuestionCreatorIOFrameworkAdapter,
    IVoteIOFrameworkAdapter,
)

from polls.question_service import DjangoQuestionRepository
from polls.choice_service import DjangoChoiceRepository

def production():
    components.registerAdapter(DjangoQuestionRepository, ICreateQuestionExecutor, IQuestionRepository)
    components.registerAdapter(DjangoChoiceRepository, ICreateChoiceExecutor, IChoiceRepository)
    components.registerAdapter(DjangoChoiceRepository, IVoteExecutor, IChoiceRepository)
    components.registerAdapter(Vote, IVoteIOFrameworkAdapter, IVoteExecutor)
    components.registerAdapter(CreateQuestion, IQuestionCreatorIOFrameworkAdapter, ICreateQuestionExecutor)
    components.registerAdapter(CreateChoice, IChoiceCreatorIOFrameworkAdapter, ICreateChoiceExecutor)
