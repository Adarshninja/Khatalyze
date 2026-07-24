from core.statement_parser import StatementParser

parser = StatementParser(
    "data/parsed/adarsh-statement.md"
)

data = parser.parse()

print(data["transactions"][:3])

parser.save(
    "data/structured/adarsh-statement.json"
)