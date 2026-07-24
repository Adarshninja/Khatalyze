from core.statement_parser import StatementParser
from core.analytics import AnalyticsEngine
from core.insights import InsightEngine
from core.risk_engine import RiskEngine
from core.recommendation_engine import RecommendationEngine
from core.llm import LLMClient
from core.rag import FinancialRAG

parser = StatementParser("data/parsed/adarsh-statement.md")

report = parser.parse()

report = AnalyticsEngine(report).generate_report()
report = InsightEngine(report).generate_report()
report = RiskEngine(report).analyze()
report = RecommendationEngine(report).generate_report()


llm = LLMClient()


rag = FinancialRAG(
    report=report,
    llm=llm,
)

# --------------------------
# Ask a question
# --------------------------

response = rag.ask(

    "Which merchant received the highest amount?"
)

print("\nQuestion:")
print(response["question"])

print("\nAnswer:")
print(response["answer"])