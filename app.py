import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import openpyxl as xl

st.set_page_config(page_title="Sales Data Analysis Dashboard", layout="wide")

st.title("📊 Sales Data Analysis Dashboard")


uploaded_file = st.file_uploader(
    "Upload Sales File",
    type=["csv", "xlsx"]
)

if uploaded_file is not None:

    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)


    df["Revenue"] = df["Quantity"] * df["Price"]


    df["Date"] = pd.to_datetime(df["Date"])
    st.sidebar.header("🔍 Filter Data")

    selected_city = st.sidebar.multiselect(
        "Select City",
        df["City"].unique(),
        default=df["City"].unique()
    )

    selected_product = st.sidebar.multiselect(
        "Select Product",
        df["Product"].unique(),
        default=df["Product"].unique()
    )

    df = df[
        (df["City"].isin(selected_city)) &
        (df["Product"].isin(selected_product))
        ]


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
    st.info("Please upload a Sales file .")