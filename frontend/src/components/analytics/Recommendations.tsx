import { Lightbulb } from "lucide-react";

const recommendations = [
  "Reduce food delivery expenses.",
  "Build a 6-month emergency fund.",
  "Invest surplus cash in SIPs.",
  "Review inactive subscriptions.",
];

export default function Recommendations() {
  return (
    <div className="rounded-2xl border border-zinc-800 bg-zinc-900/50 p-6">
      <div className="mb-5 flex items-center gap-3">
        <Lightbulb className="text-yellow-400" />
        <h2 className="text-lg font-semibold text-white">
          Recommendations
        </h2>
      </div>

      <div className="space-y-3">
        {recommendations.map((item) => (
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


