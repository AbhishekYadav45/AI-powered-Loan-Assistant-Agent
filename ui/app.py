import os
import sys
import re
import streamlit as st

# make sure we can import from project root
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

from rag.query_rag import rag_answer
from oracle_db_helper import (
    get_pending_by_customer_id,
    get_pending_by_account_no,
)


def extract_customer_id(text: str):
    # any number with 5+ digits
    match = re.search(r"\b\d{5,}\b", text)
    if match:
        return match.group(0)
    return None


st.title("💼 Loan Assistant")

query = st.text_input("Ask a question (policy or pending loan or your pending loan amount):")

if st.button("Get Answer") and query:
    with st.spinner("Processing..."):
        cust_id = extract_customer_id(query)
        q_lower = query.lower()

        # 1️⃣ Account number (10+ digits)
        if cust_id and len(cust_id) >= 10 and (
            "pending" in q_lower or "balance" in q_lower or "due" in q_lower or "amount" in q_lower
        ):
            amount = get_pending_by_account_no(cust_id)
            if amount is not None:
                response = (
                    f"For account number **{cust_id}**, the pending loan amount is "
                    f"**₹{amount:,.2f}**."
                )
            else:
                response = f"No loan record found for account number {cust_id}."

        # 2️⃣ Customer ID (5–9 digits)
        elif cust_id and 5 <= len(cust_id) < 10 and (
            "pending" in q_lower or "balance" in q_lower or "due" in q_lower or "amount" in q_lower
        ):
            amount = get_pending_by_customer_id(cust_id)
            if amount is not None:
                response = (
                    f"For customer ID **{cust_id}**, the pending loan amount is "
                    f"**₹{amount:,.2f}**."
                )
            else:
                response = f"No loan record found for customer ID {cust_id}."

        # 3️⃣ User asking about pending loan but no id given
        elif "pending" in q_lower or "balance" in q_lower or "due" in q_lower or "amount" in q_lower:
            response = (
                "To check loan pending details, please provide your "
                "*Customer ID* or *Account Number*."
            )

        # 4️⃣ Otherwise → use RAG on policy documents
        else:
            response = rag_answer(query)

    st.markdown("### 🧾 Answer")
    st.write(response)
