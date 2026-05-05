import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Aariz Finance Dashboard", layout="wide")

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>
body {
    background-color: #0b1f3a;
    color: white;
}
h1, h2, h3 {
    color: gold;
}
.stButton>button {
    background-color: gold;
    color: black;
    border-radius: 8px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- TITLE ----------------
st.title("💰 Aariz Financial Dashboard Pro")

menu = st.sidebar.radio(
    "Select Tool",
    ["EMI Calculator", "SIP Calculator", "Compound Interest"]
)

# ---------------- EMI CALCULATOR ----------------
if menu == "EMI Calculator":
    st.header("🏦 EMI Calculator with Amortization")

    col1, col2, col3 = st.columns(3)

    loan = col1.number_input("Loan Amount", 0.0)
    rate = col2.number_input("Interest Rate (%)", 0.0)
    years = col3.number_input("Tenure (Years)", 1)

    if st.button("Calculate EMI"):
        months = years * 12
        r = rate / (12 * 100)

        emi = loan * r * (1 + r)**months / ((1 + r)**months - 1)

        st.success(f"Monthly EMI: ₹ {emi:,.2f}")

        # Amortization Schedule
        balance = loan
        data = []

        for m in range(1, months + 1):
            interest = balance * r
            principal = emi - interest
            balance -= principal

            data.append([m, emi, principal, interest, balance])

        df = pd.DataFrame(data, columns=[
            "Month", "EMI", "Principal", "Interest", "Balance"
        ])

        st.subheader("📅 Amortization Table")
        st.dataframe(df)

        # Chart
        st.subheader("📊 Payment Breakdown")
        fig, ax = plt.subplots()
        ax.plot(df["Month"], df["Principal"], label="Principal")
        ax.plot(df["Month"], df["Interest"], label="Interest")
        ax.legend()
        st.pyplot(fig)

        # Download
        st.download_button("Download CSV", df.to_csv(index=False), "emi_data.csv")

# ---------------- SIP CALCULATOR ----------------
elif menu == "SIP Calculator":
    st.header("📅 SIP Growth Calculator")

    col1, col2, col3 = st.columns(3)

    monthly = col1.number_input("Monthly Investment", 0.0)
    rate = col2.number_input("Return Rate (%)", 0.0)
    years = col3.number_input("Years", 1)

    if st.button("Calculate SIP"):
        months = years * 12
        r = rate / (12 * 100)

        values = []
        total = 0

        for m in range(1, months + 1):
            total = (total + monthly) * (1 + r)
            values.append(total)

        st.success(f"Future Value: ₹ {total:,.2f}")

        # Chart
        df = pd.DataFrame({"Month": range(1, months + 1), "Value": values})

        st.subheader("📈 Investment Growth")
        fig, ax = plt.subplots()
        ax.plot(df["Month"], df["Value"])
        st.pyplot(fig)

        st.download_button("Download CSV", df.to_csv(index=False), "sip_data.csv")

# ---------------- COMPOUND INTEREST ----------------
elif menu == "Compound Interest":
    st.header("📈 Compound Interest Calculator")

    principal = st.number_input("Principal", 0.0)
    rate = st.number_input("Rate (%)", 0.0)
    years = st.number_input("Years", 1)
    n = st.selectbox("Compounding", [1, 2, 4, 12])

    if st.button("Calculate"):
        values = []
        for t in range(1, years + 1):
            amount = principal * (1 + rate/(100*n))**(n*t)
            values.append(amount)

        final_amount = values[-1]

        st.success(f"Final Amount: ₹ {final_amount:,.2f}")

        df = pd.DataFrame({
            "Year": range(1, years + 1),
            "Amount": values
        })

        st.subheader("📊 Growth Over Time")
        fig, ax = plt.subplots()
        ax.plot(df["Year"], df["Amount"])
        st.pyplot(fig)

        st.download_button("Download CSV", df.to_csv(index=False), "ci_data.csv")