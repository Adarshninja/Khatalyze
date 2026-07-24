### To build vector again :

from core.statement_parser import StatementParser
from core.analytics import AnalyticsEngine
from core.insights import InsightEngine
from core.risk_engine import RiskEngine
from core.recommendation_engine import RecommendationEngine

from core.embeddings import EmbeddingEngine
from core.vector_store import VectorStore

# --------------------------------------------
# Build Financial Report
# --------------------------------------------

parser = StatementParser("data/parsed/adarsh-statement.md")

report = parser.parse()

report = AnalyticsEngine(report).generate_report()
report = InsightEngine(report).generate_report()
report = RiskEngine(report).analyze()
report = RecommendationEngine(report).generate_report()

# --------------------------------------------
# Generate Embeddings
# --------------------------------------------

print("Generating embeddings...")

embedding_engine = EmbeddingEngine(report)

result = embedding_engine.generate_embeddings()

embeddings = result["embeddings"]
chunks = result["chunks"]

print(f"Generated {len(chunks)} chunks.")

# --------------------------------------------
# Build Vector Store
# --------------------------------------------

print("Building FAISS index...")

store = VectorStore(embeddings.shape[1])

store.add_embeddings(
    embeddings,
    chunks,
)

store.save("data/vector_db")

print("Vector database saved successfully!")

print(f"Total vectors: {len(chunks)}")