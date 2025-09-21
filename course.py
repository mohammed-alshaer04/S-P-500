import streamlit as st
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px

company_list = [
    r'AAPL_data.csv',
    r'AMZN_data.csv',
    r'GOOG_data.csv',
    r'MSFT_data.csv'
]

all_data = pd.DataFrame()

for file in company_list:
    current_data = pd.read_csv(file)
    all_data = pd.concat([all_data, current_data], ignore_index = True)

all_data['date'] = pd.to_datetime(all_data['date'])

tech_list = all_data['Name'].unique()

st.set_page_config(page_title = "Stock Analysis Dashboard", layout="wide")
st.title("Tech Stocks Analysis Dashboard")
st.sidebar.title("Choose a company")

selected_company = st.sidebar.selectbox("Select a stock", tech_list)

company_df = all_data[all_data['Name']== selected_company]
company_df.sort_values(by=['date'], inplace=True)

##first plot
st.subheader(f"1. Closing Price of {selected_company} Over Time")
fig1 = px.line(company_df, x="date", y="close",
               title= selected_company+"Closing Prices of Over Time")
st.plotly_chart(fig1, use_container_width=True)

##2nd plot
st.subheader("2. Moving Averages (10, 20, 50 days)")

ma_day = [10, 20, 50]
for ma in ma_day:
    company_df['close_'+str(ma)] = company_df['close'].rolling(ma).mean()

fig2 = px.line(company_df, x="date", y=['close_10', 'close_20',	'close_50'],
               title= selected_company+"Closing Prices With Moving Averages")
st.plotly_chart(fig2, use_container_width=True)

## 3. plot
st.subheader("3. Daily Returns For" + selected_company)
company_df['Daily return (in %)'] = company_df['close'].pct_change()*100

fig3 = px.line(company_df, x="date", y= "Daily return (in %)",
               title= "Daily Return(%)")
st.plotly_chart(fig3, use_container_width=True)

# 4. plot
st.subheader("4. Resampled Closing Prices (Monthly / Quarterly /Yearly)")
company_df.set_index('date', inplace = True)
Resample_Option = st.radio("Select Resample Frequency", ["Monthly", "Quarterly", "Yearly"])

if Resample_Option == "Monthly":
    resampled = company_df['close'].resample('ME').mean()
elif Resample_Option == "Quarterly":
    resampled = company_df['close'].resample('QE').mean()
else:
    resampled = company_df['close'].resample('YE').mean()

fig4 = px.line(resampled,
               title= selected_company+ " " + Resample_Option + " Average closing price" )
st.plotly_chart(fig4, use_container_width=True)

##fig 5
app = pd.read_csv(company_list[0])
amazon = pd.read_csv(company_list[1])
google = pd.read_csv(company_list[2])
msft = pd.read_csv(company_list[3])

closing_price = pd.DataFrame()

closing_price['apple_close'] = app['close']
closing_price['amazon_close'] = amazon['close']
closing_price['google_close'] = google['close']
closing_price['msft_close'] = msft['close']

fig5, ax1 = plt.subplots()
sns.heatmap(closing_price.corr(), annot=True, cmap= "coolwarm", ax=ax1)
st.pyplot(fig5)
st.markdown("---")

st.markdown("**Note:** This dashboard provides basic technical analysis of major tech stocks using Python")
