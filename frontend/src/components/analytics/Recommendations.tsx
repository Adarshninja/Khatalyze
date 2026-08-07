import { Lightbulb } from "lucide-react";

interface Recommendation {
  title: string;
  description: string;
}

interface RecommendationsProps {
  recommendations: Recommendation[];
}

export default function Recommendations({
  recommendations,
}: RecommendationsProps) {
  return (
    <div className="rounded-2xl border border-zinc-800 bg-zinc-900/50 p-6">
      <div className="mb-5 flex items-center gap-3">
        <Lightbulb className="text-yellow-400" />

        <h2 className="text-lg font-semibold text-white">
          Recommendations
        </h2>
      </div>

      <div className="space-y-3">
        {recommendations.map((item, index) => (
          <div
            key={index}
            className="rounded-xl bg-zinc-800/40 p-4"
          >
            <h3 className="font-semibold text-white">
              {item.title}
            </h3>

            <p className="mt-1 text-zinc-400">
              {item.description}
            </p>
          </div>
        ))}
      </div>
    </div>
  );
}

