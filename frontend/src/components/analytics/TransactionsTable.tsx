interface Transaction {
  id: string;
  merchant: string;
  category: string;
  amount: number;
  date: string;
  type: "DEBIT" | "CREDIT";
}

interface TransactionsTableProps {
  transactions: Transaction[];
}

export default function TransactionsTable({
  transactions,
}: TransactionsTableProps) {
  return (
    <div className="rounded-2xl border border-zinc-800 bg-zinc-900/50 p-6">
      <h2 className="mb-6 text-lg font-semibold text-white">
        Recent Transactions
      </h2>

      <div className="space-y-4">
        {transactions.map((item) => (
          <div
            key={item.id}
            className="flex items-center justify-between rounded-xl bg-zinc-800/40 p-4"
          >
            <div>
              <h3 className="font-medium text-white">
                {item.merchant}
              </h3>

              <p className="text-sm text-zinc-400">
                {item.category}
              </p>
            </div>

            <span
              className={`font-semibold ${
                item.type === "CREDIT"
                  ? "text-green-400"
                  : "text-red-400"
              }`}
            >
              ₹{item.amount.toLocaleString()}
            </span>
          </div>
        ))}
      </div>
    </div>
  );
}