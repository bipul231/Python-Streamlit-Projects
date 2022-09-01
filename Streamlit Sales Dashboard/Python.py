#--- How to Run ---
#--- Typy this in command line ---
#cd Desktop\PROJECT_1\streamlit-sales-dashboard-main\streamlit-sales-dashboard-main
#Then Type Streamlit run Python.py
import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Sales Dashboard", page_icon=":bar_chart:", layout="wide")
                   

df = pd.read_excel(
    io = 'super_sales.xlsx',
    engine='openpyxl',
    sheet_name='Sales',
    skiprows=3,
    usecols='B:R',
    nrows=1000,
)

#---- ADD 'hour' COLUMN TO DATAFRAME ----
df["hour"] = pd.to_datetime(df["Time"], format="%H:%M:%S").dt.hour


#-----SIDEBAR-----
st.sidebar.header("Please Filter Here:")
city = st.sidebar.multiselect(
    "Select the City:",
    options=df["City"].unique(),
    default=df["City"].unique(),
)

customer_type = st.sidebar.multiselect(
    "Select the Customer Type:",
    options=df["Customer_type"].unique(),
    default=df["Customer_type"].unique(),
)

gender = st.sidebar.multiselect(
    "Select the Gender:",
    options=df["Gender"].unique(),
    default=df["Gender"].unique(),
)

df_selection = df.query(
    "City == @city & Customer_type == @customer_type & Gender == @gender"
)

#st.dataframe(df_selection)

#----MAINPAGE----
st.title(":bar_chart: Sales Dashboard")
st.markdown("##")

#----TOP KPI's----
total_sales = int(df_selection["Total"].sum())
average_rating = round(df_selection["Rating"].mean(),1)
star_rating = ":star:" * int(round(average_rating,0))
average_sale_by_transaction = round(df_selection["Total"].mean(),2)


left_column, middle_column, right_column = st.columns(3)
with left_column:
    st.subheader("Total Sales:")
    st.subheader(f"US $ {total_sales:,}") #---seperated by thousand places---
with middle_column:
    st.subheader("Average Rating:")
    st.subheader(f"{average_rating} {star_rating}")
with right_column:
    st.subheader("Average Sales Per Transaction:")
    st.subheader(f"US $ {average_sale_by_transaction}")

st.markdown("---")

#--- SALES BY PRODUCT LINE [BAR CHART] ---

#---- GROUP  BY IN PANDAS : ----

#---- IT WILL GROUP BY ALL NUMARIC VALUES ----
#df.groupby(by=["Product line"].sum())

#---- GROUP BY IN RELATION TO TOTAL ----
#df.groupby(by=["Product line"].sum()[["Total"]])

#---- GROUP BY IN RELATION TO TOTAL AND THEN SORT ACC TO TOTAL ----
#df.groupby(by=["Product line"].sum()[["Total"]].sort_values(by="Total"))

sales_by_product_line = (
    df_selection.groupby(by=["Product line"]).sum()[["Total"]].sort_values(by="Total")
)

#----USE PLOTLY EXPRESS LIBREARY TO PLOT THE DATA----
fig_product_sales = px.bar(
    sales_by_product_line,
    x = "Total",
    y = sales_by_product_line.index,
    orientation = "h",
    title = "<b>Sales by Product Line</b>",
    color_discrete_sequence=["#A9DFBF"] * len(sales_by_product_line),
    template="plotly_white",
)
fig_product_sales.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False))
)



#---- SALES BY HOUR [BAR CHART] ----
sales_by_hour = df_selection.groupby(by=["hour"]).sum()[["Total"]]
fig_hourly_sales = px.bar(
    sales_by_hour,
    x=sales_by_hour.index,
    y="Total",
    title="<b>Sales by hour</b>",
    color_discrete_sequence=["#A9DFBF"] * len(sales_by_hour),
    template="plotly_white",
)
fig_hourly_sales.update_layout(
    xaxis=dict(tickmode="linear"),
    plot_bgcolor="rgba(0,0,0,0)",
    yaxis=(dict(showgrid=False)),
)

#---- Side by Side Graph ----
left_column, right_column = st.columns(2)
left_column.plotly_chart(fig_hourly_sales, use_container_width=True)
right_column.plotly_chart(fig_product_sales, use_container_width=True)

# ---- HIDE STREAMLIT STYLE ----
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

#primaryColor = "#2b2547"
#backgroundColor = "#00172B"
#secondaryBackgroundColor = "#0083B8"

