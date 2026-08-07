# from core.question_router import QuestionRouter

# questions = [
#     "Is this a credit card statement?",
#     "Which bank issued this statement?",
#     "What is the statement period?",
#     "Who is the account holder?",
#     "How much did I spend this month?",
#     "Which merchant received the most money?",
#     "Why am I overspending?",
#     "Give me financial advice."
# ]

# for q in questions:
#     route = QuestionRouter.classify(q)
#     print(f"{q}\n -> {route.value}\n")
    
    
    
from core.statement_parser import StatementParser
from core.metadata_answerer import MetadataAnswerer

parser = StatementParser("data/parsed/6226ce483b094ac09abdc0d8c3642175.md")   # your parsed markdown

report = parser.parse()

questions = [
    "Is this credit card or debit card statement?",
    "Which bank issued this statement?",
    "Who is the account holder?",
    "What is the statement period?"
]

for q in questions:
    print(q)
    print(MetadataAnswerer.answer(q, report))
    print("-" * 50)