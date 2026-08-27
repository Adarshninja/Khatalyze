"""
core/llm.py

LLM wrapper for Khatalyse AI.
Currently supports Groq.
"""

from __future__ import annotations

import os

from dotenv import load_dotenv
from groq import Groq

load_dotenv(override=True)


class LLMClient:
    """
    Wrapper around Groq's Chat Completion API.
    """

    def __init__(
        self,
        # model: str = "llama-3.3-70b-versatile",
        model: str = "openai/gpt-oss-120b",
        temperature: float = 0.2,
    ):
        api_key = os.getenv("GROQ_API_KEY")

        if not api_key:
            raise ValueError(
                "GROQ_API_KEY not found in .env file."
            )

        self.client = Groq(api_key=api_key)
        self.model = model
        self.temperature = temperature

    def generate(self, prompt: str) -> str:
        response = self.client.chat.completions.create(
            model=self.model,
            temperature=self.temperature,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are FinSight AI, an expert financial assistant. "
                        "Answer ONLY using the provided financial context. "
                        "Do not fabricate information. "
                        "If the answer is unavailable, clearly say so."
                    ),
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
        )

        return response.choices[0].message.content.strip()
