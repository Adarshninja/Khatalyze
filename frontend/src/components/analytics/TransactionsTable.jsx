const transactions = [
  {
    merchant: "Amazon",
    category: "Shopping",
    amount: "-$120",
  },
  {
    merchant: "Starbucks",
    category: "Food",
    amount: "-$18",
  },
  {
    merchant: "Salary",
    category: "Income",
    amount: "+$3,200",
  },
];

export default function TransactionsTable() {
  return (
    <div className="rounded-2xl border border-zinc-800 bg-zinc-900/50 p-6">
      <h2 className="mb-6 text-lg font-semibold text-white">
        Recent Transactions
      </h2>

      <div className="space-y-4">
        {transactions.map((item) => (
          <div
            key={`${item.merchant}-${item.amount}`}
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

            <span className="font-semibold text-white">
              {item.amount}
            </span>
          </div>
        ))}
      </div>
    </div>
  );
}




