import sys
from pathlib import Path


from core.statement_parser import StatementParser
from core.analytics import AnalyticsEngine
from core.insights import InsightEngine
from core.risk_engine import RiskEngine
from core.recommendation_engine import RecommendationEngine

from core.llm import LLMClient
from core.rag import FinancialRAG

# ----------------------------------------
# Build Financial Report
# ----------------------------------------

parser = StatementParser("data/parsed/adarsh-statement.md")

report = parser.parse()

report = AnalyticsEngine(report).generate_report()
report = InsightEngine(report).generate_report()
report = RiskEngine(report).analyze()
report = RecommendationEngine(report).generate_report()

# ----------------------------------------
# Initialize RAG
# ----------------------------------------

rag = FinancialRAG(
    report=report,
    llm=LLMClient()
)

# ----------------------------------------
# Test Questions
# ----------------------------------------

questions = [

    # Spending
    "How much money was spent through UPI?",
    "What is my total expenditure?",
    "What is my total income?",
    "Which category has the highest spending?",
    "How much cash was withdrawn?",

    # Merchant
    "Which merchant received the highest amount?",
    "List my top 5 merchants.",
    "How many transactions did I make with Amazon?",
    "Who is my most frequent payee?",

    # Transactions
    "Show my latest transaction.",
    "List all transactions above ₹5000.",
    "What happened on 10 January?",

    # Insights
    "What are my spending habits?",
    "What financial insights do you have?",
    "Did I spend more than I earned?",

    # Risk
    "Did you detect any financial risks?",
    "Am I overspending?",
    "What are the risk flags?",

    # Recommendation
    "How can I save more money?",
    "What recommendations do you have for me?",

    # Negative Tests
    "What is my credit score?",
    "What is my PAN number?",
    "Which EMI am I paying?"
]

# ----------------------------------------
# Run Benchmark
# ----------------------------------------

for i, question in enumerate(questions, start=1):

    print("=" * 100)
    print(f"TEST {i}")
    print("=" * 100)

    print(f"\nQuestion:\n{question}\n")

    response = rag.ask(question)

    print("Answer:\n")
    print(response["answer"])

    print("\n")
    
