import { Sparkles } from "lucide-react";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";

export default function Chat() {
  return (
    <div className="flex h-full flex-1 flex-col bg-[#09090B]">

      {/* Header */}
      <div className="border-b border-white/10 p-8">

        <div className="flex items-center gap-3">

          <Sparkles className="text-cyan-400"/>

          <div>

            <h1 className="text-3xl font-bold text-white">
              AI Workspace
            </h1>

            <p className="text-zinc-400">
              Ask anything about your finances.
            </p>

          </div>

        </div>

      </div>

      {/* Messages */}

      <div className="flex-1 space-y-6 overflow-auto p-8">

        <div className="max-w-xl rounded-3xl bg-cyan-500/10 p-5 text-cyan-300">
          Which merchant did I spend the most on?
        </div>

        <div className="max-w-2xl rounded-3xl border border-white/10 bg-[#111113] p-6 text-zinc-300">

          You spent approximately
          <span className="font-semibold text-cyan-400">
            {" "} ₹420 {" "}
          </span>

          at Amazon across eight transactions during January.

        </div>

      </div>

      {/* Input */}

      <div className="border-t border-white/10 p-6">

        <div className="flex gap-4">

          <Input
            placeholder="Ask Khatalyse..."
          />

          <Button>
            Send
          </Button>

        </div>

      </div>

    </div>
  );
}

