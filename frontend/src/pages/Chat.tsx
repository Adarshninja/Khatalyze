import { useEffect, useRef, useState } from "react";
import { Sparkles, Loader2 } from "lucide-react";

import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";

import { useChat } from "@/hooks/useChat";
import { useCurrentStatement } from "@/context/CurrentStatementContext";

type Message = {
  role: "user" | "assistant";
  text: string;
};

export default function Chat() {
  const { statementId } = useCurrentStatement();

  const chat = useChat(statementId ?? "");

  const [question, setQuestion] = useState("");

  const [messages, setMessages] = useState<Message[]>([
    {
      role: "assistant",
      text: "Hi! I'm Khatalyse AI. Ask me anything about your statement.",
    },
  ]);

  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({
      behavior: "smooth",
    });
  }, [messages]);

  async function sendMessage() {
    const text = question.trim();

    if (!text) return;

    if (!statementId) {
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          text: "Please upload and analyze a statement first.",
        },
      ]);
      return;
    }

    if (chat.isPending) return;

    setMessages((prev) => [
      ...prev,
      {
        role: "user",
        text,
      },
    ]);

    setQuestion("");

    try {
      const response = await chat.mutateAsync(text);

      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          text:
            response.answer ??
            "Sorry, I couldn't generate a response.",
        },
      ]);
    } catch (error) {
      console.error(error);

      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          text: "Unable to contact the backend.",
        },
      ]);
    }
  }

  return (
    <div className="flex flex-1 flex-col bg-[#09090B] h-full">

      <div className="border-b border-white/10 p-8">
        <div className="flex items-center gap-3">
          <Sparkles className="text-cyan-400" />

          <div>
            <h1 className="text-3xl font-bold text-white">
              AI Workspace
            </h1>

            <p className="text-zinc-400">
              Ask anything about your financial statement.
            </p>
          </div>
        </div>
      </div>

      <div className="flex-1 overflow-auto space-y-6 p-8">

        {messages.map((msg, index) => (
          <div
            key={index}
            className={`flex ${
              msg.role === "user"
                ? "justify-end"
                : "justify-start"
            }`}
          >
            <div
              className={`max-w-2xl whitespace-pre-wrap rounded-3xl px-5 py-4 ${
                msg.role === "user"
                  ? "bg-cyan-500 text-white"
                  : "border border-white/10 bg-[#111113] text-zinc-300"
              }`}
            >
              {msg.text}
            </div>
          </div>
        ))}

        {chat.isPending && (
          <div className="flex">
            <div className="flex items-center gap-2 rounded-3xl border border-white/10 bg-[#111113] px-5 py-4 text-zinc-400">
              <Loader2
                className="animate-spin"
                size={18}
              />

              Khatalyse is thinking...
            </div>
          </div>
        )}

        <div ref={bottomRef} />
      </div>

      <div className="border-t border-white/10 p-6">
        <div className="flex gap-4">

          <Input
            placeholder="Ask Khatalyse..."
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === "Enter") {
                sendMessage();
              }
            }}
          />

          <Button
            onClick={sendMessage}
            disabled={chat.isPending || !statementId}
          >
            {chat.isPending ? "..." : "Send"}
          </Button>

        </div>
      </div>

    </div>
  );
}