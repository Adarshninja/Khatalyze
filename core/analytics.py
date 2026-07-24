from __future__ import annotations

import json
from pathlib import Path
from collections import Counter
from typing import Any

import pandas as pd


class AnalyticsEngine:
    """
    FinSight AI Analytics Engine
    """

    def __init__(self, json_path: str | Path):
        self.json_path = Path(json_path)

        with open(self.json_path, "r", encoding="utf-8") as f:
            self.statement = json.load(f)

        self.transactions = self.statement.get("transactions", [])
        self.df = pd.DataFrame(self.transactions)
        self._prepare_dataframe()

    def _prepare_dataframe(self):
        if self.df.empty:
            return

        defaults = {
            "date": None,
            "description": "",
            "type": "",
            "amount": 0,
            "balance": 0,
            "category": "Others",
            "party": "Unknown",
            "mode": "",
            "bank": "",
        }

        for k, v in defaults.items():
            if k not in self.df.columns:
                self.df[k] = v

        self.df["date"] = pd.to_datetime(
            self.df["date"],
            format="%d-%m-%y",
            errors="coerce")
        self.df["amount"] = pd.to_numeric(self.df["amount"], errors="coerce").fillna(0.0)
        self.df["balance"] = pd.to_numeric(self.df["balance"], errors="coerce").fillna(0.0)

        self.df["type"] = (
            self.df["type"]
            .astype(str)
            .str.strip()
            .str.lower()
            .replace({"dr": "debit", "cr": "credit"})
        )

        self.df["category"] = self.df["category"].fillna("Others").astype(str).str.strip()
        self.df["party"] = self.df["party"].fillna("Unknown").astype(str).str.strip()

        self.df["month"] = self.df["date"].dt.to_period("M").astype(str)
        self.df["weekday"] = self.df["date"].dt.day_name()

    def _filter(self, t: str):
        return self.df[self.df["type"] == t]

    def total_income(self):
        return float(self._filter("credit")["amount"].sum())

    def total_expense(self):
        return float(self._filter("debit")["amount"].sum())

    def net_cash_flow(self):
        return self.total_income() - self.total_expense()

    def average_credit(self):
        d = self._filter("credit")
        return 0 if d.empty else float(d["amount"].mean())

    def average_debit(self):
        d = self._filter("debit")
        return 0 if d.empty else float(d["amount"].mean())

    def largest_credit(self):
        d = self._filter("credit")
        return {} if d.empty else d.loc[d["amount"].idxmax()].to_dict()

    def largest_debit(self):
        d = self._filter("debit")
        return {} if d.empty else d.loc[d["amount"].idxmax()].to_dict()

    def spending_by_category(self):
        d = self._filter("debit")
        if d.empty:
            return {}
        return d.groupby("category")["amount"].sum().sort_values(ascending=False).to_dict()

    def income_by_category(self):
        d = self._filter("credit")
        if d.empty:
            return {}
        return d.groupby("category")["amount"].sum().sort_values(ascending=False).to_dict()

    def monthly_summary(self):
        if self.df.empty:
            return {}
        g = self.df.groupby(["month", "type"])["amount"].sum().unstack(fill_value=0)
        out = {}
        for m in g.index:
            income = float(g.loc[m].get("credit", 0))
            expense = float(g.loc[m].get("debit", 0))
            out[m] = {
                "income": income,
                "expense": expense,
                "savings": income - expense,
            }
        return out

    def daily_spending(self):
        d = self._filter("debit")
        if d.empty:
            return {}
        s = d.groupby(d["date"].dt.date)["amount"].sum()
        return {str(k): float(v) for k, v in s.items()}

    def merchant_statistics(self):
        d = self._filter("debit")
        if d.empty:
            return {}
        res = (
            d.groupby("party")
            .agg(
                transaction_count=("party", "count"),
                total_spent=("amount", "sum"),
                average_transaction=("amount", "mean"),
            )
            .sort_values("total_spent", ascending=False)
            .round(2)
        )
        return res.to_dict("index")

    def recurring_transactions(self):
        if self.df.empty:
            return []
        out = []
        for party, grp in self.df.groupby("party"):
            if len(grp) >= 3:
                out.append({
                    "party": party,
                    "count": int(len(grp)),
                    "average_amount": float(grp["amount"].mean())
                })
        return sorted(out, key=lambda x: x["count"], reverse=True)

    def cash_flow_trend(self):
        if self.df.empty:
            return []
        out = []
        prev = None
        for _, r in self.df.sort_values("date").iterrows():
            bal = float(r["balance"])
            out.append({
                "date": str(r["date"].date()) if pd.notna(r["date"]) else "",
                "balance": bal,
                "change": 0 if prev is None else bal - prev
            })
            prev = bal
        return out

    def behavioural_insights(self):
        d = self._filter("debit")
        if d.empty:
            return {}
        cat = self.spending_by_category()
        return {
            "highest_spending_day": d.groupby("weekday")["amount"].sum().idxmax(),
            "average_daily_spending": float(d.groupby(d["date"].dt.date)["amount"].sum().mean()),
            "largest_purchase": float(d["amount"].max()),
            "most_used_category": max(cat, key=cat.get) if cat else None,
        }

    def financial_risk_flags(self):
        flags = []
        d = self._filter("debit")
        if not d.empty and d["amount"].max() > d["amount"].mean() * 4:
            flags.append("Unusually large expense detected.")
        if (self.df["balance"] < 1000).sum():
            flags.append(f"Balance below ₹1000 occurred {(self.df['balance'] < 1000).sum()} times.")
        atm = self.df[self.df["description"].str.contains("ATM", case=False, na=False)]
        if len(atm) >= 5:
            flags.append("Frequent ATM withdrawals detected.")
        return flags

    def generate_report(self) -> dict[str, Any]:
        return {
            "kpis": {
                "income": self.total_income(),
                "expense": self.total_expense(),
                "net_cash_flow": self.net_cash_flow(),
                "average_credit": self.average_credit(),
                "average_debit": self.average_debit(),
            },
            "category_analysis": {
                "income": self.income_by_category(),
                "spending": self.spending_by_category(),
            },
            "monthly_summary": self.monthly_summary(),
            "daily_spending": self.daily_spending(),
            "merchant_statistics": self.merchant_statistics(),
            "largest_credit": self.largest_credit(),
            "largest_debit": self.largest_debit(),
            "recurring_transactions": self.recurring_transactions(),
            "cash_flow": self.cash_flow_trend(),
            "behavioural_insights": self.behavioural_insights(),
            "risk_flags": self.financial_risk_flags(),
        }
