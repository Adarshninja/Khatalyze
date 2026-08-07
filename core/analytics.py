
"""
analytics.py

Compatibility Analytics Engine for FinSight AI.

Supports:
    AnalyticsEngine("statement.json")      # Legacy
    AnalyticsEngine(FinancialReport)       # New architecture
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any
import pandas as pd

from models.report import FinancialReport


class AnalyticsEngine:

    def __init__(self, source):
        self.report = None

        if isinstance(source, FinancialReport):
            self.report = source
            self.transactions = [t.to_dict() for t in source.transactions]
        else:
            source = Path(source)
            with open(source, "r", encoding="utf-8") as f:
                statement = json.load(f)
            self.transactions = statement.get("transactions", [])

        print("="*60)
        print("Transactions:", len(self.transactions))
        print(self.transactions[:2])
        print("="*60)
        self.df = pd.DataFrame(self.transactions)
        print(self.df.columns.tolist())
        self._prepare_dataframe()

    def _prepare_dataframe(self):
        if self.df.empty:
            return

        defaults = {
            "date": None,
            "description": "",
            "transaction_type": "",
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

        # Compatibility: old dicts used "type", new Transaction model uses "transaction_type"
        if "type" not in self.df.columns and "transaction_type" in self.df.columns:
            self.df["type"] = self.df["transaction_type"]
        elif "transaction_type" not in self.df.columns and "type" in self.df.columns:
            self.df["transaction_type"] = self.df["type"]

        self.df["date"] = pd.to_datetime(self.df["date"], errors="coerce")
        self.df["amount"] = pd.to_numeric(self.df["amount"], errors="coerce").fillna(0)
        self.df["balance"] = pd.to_numeric(self.df["balance"], errors="coerce").fillna(0)
        self.df["type"] = (
            self.df["type"].astype(str).str.strip().str.lower()
            .replace({
                "cr":"credit","dr":"debit",
                "credit":"credit","debit":"debit",
                "transactiontype.credit":"credit",
                "transactiontype.debit":"debit"
            })
        )
        self.df["category"] = self.df["category"].fillna("Others").astype(str)
        self.df["party"] = self.df["party"].fillna("Unknown").astype(str)
        self.df["month"] = self.df["date"].dt.to_period("M").astype(str)
        self.df["weekday"] = self.df["date"].dt.day_name()

    def _filter(self, t):
        return self.df[self.df["type"] == t]

    def total_income(self): return float(self._filter("credit")["amount"].sum())
    def total_expense(self): return float(self._filter("debit")["amount"].sum())
    def net_cash_flow(self): return self.total_income()-self.total_expense()
    def average_credit(self):
        d=self._filter("credit"); return 0 if d.empty else float(d["amount"].mean())
    def average_debit(self):
        d=self._filter("debit"); return 0 if d.empty else float(d["amount"].mean())
    def largest_credit(self):
        d=self._filter("credit")
        if d.empty:
            return {}
        row = d.loc[d["amount"].idxmax()].to_dict()
        
        for k, v in row.items():
            if hasattr(v, "isoformat"):
                row[k] = v.isoformat()
        return row
    
    def largest_debit(self):
        d=self._filter("debit")
        
        if d.empty:
            return {}
        row = d.loc[d["amount"].idxmax()].to_dict()
        
        for k, v in row.items():
            if hasattr(v, "isoformat"):
                row[k] = v.isoformat()
        return row

    def spending_by_category(self):
        d=self._filter("debit")
        return {} if d.empty else d.groupby("category")["amount"].sum().sort_values(ascending=False).to_dict()

    def income_by_category(self):
        d=self._filter("credit")
        return {} if d.empty else d.groupby("category")["amount"].sum().sort_values(ascending=False).to_dict()

    def monthly_summary(self):
        if self.df.empty: return {}
        g=self.df.groupby(["month","type"])["amount"].sum().unstack(fill_value=0)
        out={}
        for m in g.index:
            inc=float(g.loc[m].get("credit",0)); exp=float(g.loc[m].get("debit",0))
            out[m]={"income":inc,"expense":exp,"savings":inc-exp}
        return out

    def daily_spending(self):
        d=self._filter("debit")
        if d.empty:return {}
        s=d.groupby(d["date"].dt.date)["amount"].sum()
        return {str(k):float(v) for k,v in s.items()}

    def merchant_statistics(self):
        d=self._filter("debit")
        if d.empty:return {}
        return d.groupby("party").agg(
            transaction_count=("party","count"),
            total_spent=("amount","sum"),
            average_transaction=("amount","mean")
        ).sort_values("total_spent",ascending=False).round(2).to_dict("index")

    def recurring_transactions(self):
        if self.df.empty:return []
        out=[]
        for party,g in self.df.groupby("party"):
            if len(g)>=3:
                out.append({"party":party,"count":int(len(g)),"average_amount":float(g["amount"].mean())})
        return sorted(out,key=lambda x:x["count"],reverse=True)

    def cash_flow_trend(self):
        if self.df.empty:return []
        out=[];prev=None
        for _,r in self.df.sort_values("date").iterrows():
            bal=float(r["balance"])
            out.append({"date":str(r["date"].date()) if pd.notna(r["date"]) else "","balance":bal,"change":0 if prev is None else bal-prev})
            prev=bal
        return out

    def behavioural_insights(self):
        d=self._filter("debit")
        if d.empty:return {}
        cat=self.spending_by_category()
        return {
            "highest_spending_day": d.groupby("weekday")["amount"].sum().idxmax(),
            "average_daily_spending": float(d.groupby(d["date"].dt.date)["amount"].sum().mean()),
            "largest_purchase": float(d["amount"].max()),
            "most_used_category": max(cat,key=cat.get) if cat else None,
        }

    def financial_risk_flags(self):
        flags=[]
        d=self._filter("debit")
        if not d.empty and d["amount"].max()>d["amount"].mean()*4:
            flags.append("Unusually large expense detected.")
        if (self.df["balance"]<1000).sum():
            flags.append(f"Balance below ₹1000 occurred {(self.df['balance']<1000).sum()} times.")
        atm=self.df[self.df["description"].str.contains("ATM",case=False,na=False)]
        if len(atm)>=5:
            flags.append("Frequent ATM withdrawals detected.")
        return flags

    def generate_report(self):
        analytics={
            "kpis":{
                "income":self.total_income(),
                "expense":self.total_expense(),
                "net_cash_flow":self.net_cash_flow(),
                "average_credit":self.average_credit(),
                "average_debit":self.average_debit(),
            },
            "category_analysis":{"income":self.income_by_category(),"spending":self.spending_by_category()},
            "monthly_summary":self.monthly_summary(),
            "daily_spending":self.daily_spending(),
            "merchant_statistics":self.merchant_statistics(),
            "largest_credit":self.largest_credit(),
            "largest_debit":self.largest_debit(),
            "recurring_transactions":self.recurring_transactions(),
            "cash_flow":self.cash_flow_trend(),
            "behavioural_insights":self.behavioural_insights(),
            "risk_flags":self.financial_risk_flags(),
        }

        if self.report is None:
            return analytics

        self.report.kpis=analytics["kpis"]
        self.report.category_analysis=analytics["category_analysis"]
        self.report.monthly_summary=analytics["monthly_summary"]
        self.report.merchant_statistics=analytics["merchant_statistics"]
        self.report.cashflow_analysis={
            "daily_spending":analytics["daily_spending"],
            "cash_flow":analytics["cash_flow"]
        }
        self.report.behavioural_insights=analytics["behavioural_insights"]
        self.report.recurring_transactions=analytics["recurring_transactions"]
        self.report.metadata["largest_credit"]=analytics["largest_credit"]
        self.report.metadata["largest_debit"]=analytics["largest_debit"]
        self.report.metadata["risk_flags"]=analytics["risk_flags"]

        return self.report
