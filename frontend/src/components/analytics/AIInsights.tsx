import { Sparkles } from "lucide-react";

const insights = [
  "Food spending increased by 18% this month.",
  "You received your highest salary in the last six months.",
  "Three recurring subscriptions were detected.",
  "Weekend expenses are significantly higher than weekdays.",
];

export default function AIInsights() {
  return (
    <div className="rounded-2xl border border-zinc-800 bg-zinc-900/50 p-6">
      <div className="mb-5 flex items-center gap-3">
        <Sparkles className="text-cyan-400" />
        <h2 className="text-lg font-semibold text-white">
          AI Insights
        </h2>
      </div>

      <div className="space-y-3">
        {insights.map((item) => (
          <div
            key={item}
            className="rounded-xl bg-zinc-800/40 p-4 text-zinc-300"
          >
            {item}
          </div>
        ))}
      </div>
    </div>
  );
}


