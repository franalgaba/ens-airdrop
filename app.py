import json
import wget
import pandas as pd
import numpy as np

import plotly.express as px
import streamlit as st

st.title("ENS Airdrop Check")
st.text("Insert you Ethereum address below:")

wget.download("https://raw.githubusercontent.com/ensdomains/governance/420b2ce24ca18eba2ff2d13da40520be49f98923/airdrop.json")

data = []
for line in open("./airdrop.json").readlines():
  data.append(json.loads(line))
df = pd.DataFrame(data)
df['past_tokens'] = df['past_tokens'].astype(float)
df['future_tokens'] = df['future_tokens'].astype(float)
df["balance"] = (df['past_tokens'] + df['future_tokens']) / 10**18

owner = st.text_input("")

placeholder = st.empty()

if owner != "":
  result = df.loc[df['owner'].eq(owner.lower())]
  if len(result.index) == 0:
    placeholder.text(f"The address {owner} is not available for the ENS Token airdrop")
  else:
    placeholder.text(f"Claimable airdrop: {result['balance'].values[0]} ENS")

st.title("ENS Airdrop Distribution")

option = st.selectbox(label="Truncated number of ENS tokens", options=[10, 25, 50, 75, 100])

# Here we use a column with categorical data
result = df["balance"].apply(lambda x: x - (x % option) )
fig = px.histogram(data_frame=result, x="balance")
st.plotly_chart(fig)
