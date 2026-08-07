import { Sparkles } from "lucide-react";

interface AIInsightsProps {
  insights: string[];
}

export default function AIInsights({
  insights,
}: AIInsightsProps) {
  return (
    <div className="rounded-2xl border border-zinc-800 bg-zinc-900/50 p-6">
      <div className="mb-5 flex items-center gap-3">
        <Sparkles className="text-cyan-400" />

        <h2 className="text-lg font-semibold text-white">
          AI Insights
        </h2>
      </div>

      <div className="space-y-3">
        {insights.map((item, index) => (
          <div
            key={index}
            className="rounded-xl bg-zinc-800/40 p-4 text-zinc-300"
          >
            {item}
          </div>
        ))}
      </div>
    </div>
  );
}

