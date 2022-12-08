import streamlit as st
import pandas as pd
import plotly.express as px


st.set_page_config(page_title='Visualisation Of Crimes Data In USA')

df = pd.read_csv('crimedata.csv')

st.header("Correlation between PolicAveOTWorked and assaultPerPop")

# SELECT BY State
states = df["state"].unique().tolist()
states_selector = st.multiselect('State', states, default=states)

# SELECT BY PolicAveOTWorked
df1 = df[~pd.isnull(df['PolicPerPop'])]
hours_worked = df1["PolicAveOTWorked"].unique().tolist()
hours_selector = st.slider("Police Average Hours Of Time Overworked", min_value=min(hours_worked),
                           max_value=max(hours_worked),
                           value=(min(hours_worked), max(hours_worked)))
police_mask = (df1['PolicAveOTWorked'].between(*hours_selector)) & (df1['state'].isin(states_selector))
number_of_results = df1[police_mask].shape[0]
st.markdown(f'*Available Results: {number_of_results}*')

bar_chart = px.scatter(df1[police_mask],
                       x='RacialMatchCommPol',
                       y='assaultPerPop', color_discrete_sequence=['#F63366'])
bar_chart.update_layout(yaxis_range=[0, 5000], title='Correlation between RacialMatchInPolice and assaultsPer100K')
st.plotly_chart(bar_chart)

st.header("Correlation between PctPopUnderPov and robbbPerPop")

# SELECT BY AsiansPct
racePctAsian = df["racePctAsian"].unique().tolist()
asian_selection = st.slider("Pecent of Asian Population", min_value=min(racePctAsian), max_value=max(racePctAsian),
                            value=(min(racePctAsian), max(racePctAsian)))
asian_mask = df['racePctAsian'].between(*asian_selection)

poverty_chart = px.scatter(df[asian_mask],
                           x='PctPopUnderPov',
                           y='robbbPerPop', color_discrete_sequence=['black'])
poverty_chart.update_layout(yaxis_range=[0, 2500])
st.plotly_chart(poverty_chart)


# SELECT BY Crime Type
st.header('Correlation between Requests Sent To Police and crimesPerPop')
selector = st.selectbox('Correlation between Requests Sent To Police and crimesPerPop', ('murders', 'rapes'))
if selector == "murders":
    mud_chart = px.scatter(df,
                           x='PolicReqPerOffic',
                           y='murdPerPop')
    mud_chart.update_layout(yaxis_range=[0, 100], title='Correlation between PolicReqPerOffic and murdPerPop')
    st.plotly_chart(mud_chart)
else:
    rape_chart = px.scatter(df,
                           x='PolicReqPerOffic',
                           y='rapesPerPop', color_discrete_sequence=['#F63366'])
    rape_chart.update_layout(yaxis_range=[0, 200], title='Correlation between requests to police and rapesPerPop')
    st.plotly_chart(rape_chart)

st.header("Correlation between PctUsePubTrans and autoTheftPerPop")
st.markdown("SELECT by Income")
# SELECT BY INCOME
medIncome = df["medIncome"].unique().tolist()
income_selection = st.slider("medIncome of household in US Dollars", min_value=min(medIncome), max_value=max(medIncome),
                             value=(min(medIncome), max(medIncome)))
income_mask = df['medIncome'].between(*income_selection)
number_of_results2 = df[income_mask].shape[0]
st.markdown(f'*Available Results: {number_of_results2}*')
auto_chart = px.scatter(df[income_mask],
                        x='PctUsePubTrans',
                        y='autoTheftPerPop',
                        color_discrete_sequence=['black'])
auto_chart.update_layout(yaxis_range=[0, 5500], title='Correlation between PctUsePubTrans and autoTheftPerPop')
st.plotly_chart(auto_chart)

