import streamlit as st
import pandas as pd

df = pd.read_csv("skincare.csv")

st.title("Skincare Brand Overview")

st.subheader("Full Dataset")

df_fix = df.drop(columns=['Link']) #Clean up the DataFrame by removing unnecessary columns, plan to add links elsewhere
df_st = df_fix.drop(columns=['Public Record Criticisms+'])

df_st.index = df_st.index + 1 #Adjust index to start at 1 instead of 0

st.dataframe(df_st) #Display the full DataFrame

st.subheader("Explore by Brand")

brand_column = 'Brand'  
brands = df_st[brand_column].dropna() 

selected_brand = st.selectbox("Choose a brand", brands)

brand_details = df_st[df_st[brand_column] == selected_brand] #Filter the DataFrame to show only the selected brand

st.write(f"Details for **{selected_brand}**:")
st.dataframe(brand_details) #Display the details for the selected brand

