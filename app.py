import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


st.set_page_config(page_title="Sales Data Analysis Dashboard", layout="wide")

st.title("📊 Sales Data Analysis Dashboard")


uploaded_file = st.file_uploader("Upload Sales CSV File", type=["csv"])

if uploaded_file is not None:


    df = pd.read_csv(uploaded_file)


    df["Revenue"] = df["Quantity"] * df["Price"]


    df["Date"] = pd.to_datetime(df["Date"])


    st.subheader("Dataset Preview")
    st.dataframe(df.head(20))


    total_revenue = df["Revenue"].sum()
    total_orders = len(df)
    total_products = df["Product"].nunique()

    col1, col2, col3 = st.columns(3)

    col1.metric("💰 Total Revenue", f"₹{total_revenue:,.0f}")
    col2.metric("🛒 Total Orders", total_orders)
    col3.metric("📦 Total Products", total_products)

    st.divider()


    st.subheader("🏆 Top Selling Products")

    product_sales = (
        df.groupby("Product")["Revenue"]
        .sum()
        .sort_values(ascending=False)
    )

    st.bar_chart(product_sales)

    st.divider()


    st.subheader("📈 Monthly Sales")

    df["Month"] = df["Date"].dt.strftime("%B")

    month_order = [
        "January","February","March","April","May","June",
        "July","August","September","October","November","December"
    ]

    monthly_sales = (
        df.groupby("Month")["Revenue"]
        .sum()
        .reindex(month_order)
    )

    st.line_chart(monthly_sales)

    st.divider()


    st.subheader("🌍 City Wise Sales")

    city_sales = (
        df.groupby("City")["Revenue"]
        .sum()
    )

    fig, ax = plt.subplots(figsize=(7,7))

    ax.pie(
        city_sales,
        labels=city_sales.index,
        autopct="%1.1f%%",
        startangle=90
    )

    ax.set_title("Revenue by City")

    st.pyplot(fig)

    st.divider()


    with st.expander("View Complete Dataset"):
        st.dataframe(df)

else:
    st.info("Please upload a Sales CSV file.")