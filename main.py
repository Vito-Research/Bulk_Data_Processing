import streamlit as st
import pandas as pd
import os
import datetime
def convert_df(df):
     # IMPORTANT: Cache the conversion to prevent computation on every rerun
     return df.to_csv().encode('utf-8')

uploaded_file = st.file_uploader("Choose a file")
allDF = pd.DataFrame()
if uploaded_file is not None:
    dfUploaded = pd.read_csv(uploaded_file)
    for index, row in dfUploaded.iterrows():
        rowID = row["Participant ID"]
     
        df = pd.DataFrame()
        try:
            df = pd.read_csv(("./COVID-19-Phase2-Wearables-2/" + rowID + "/Orig_Fitbit_HR.csv"))
           
        except:
            try:
                 df = pd.read_csv(("./COVID-19-Phase2-Wearables-2/" + rowID + "/Orig_NonFitbit_HR.csv"))
            except:
                st.write(("./COVID-19-Phase2-Wearables-2/" + rowID + "/Orig_Fitbit_HR.csv"))
        try:
            
            row["COVID-19 Test Date"] = pd.to_datetime(row["COVID-19 Test Date"])
            df["datetime"] = pd.to_datetime(df["datetime"])
            date1 = row["COVID-19 Test Date"] + datetime.timedelta(days=-3)
            date2 = row["COVID-19 Test Date"] + datetime.timedelta(days=3)
            
            df = df[df["datetime"].dt.hour < 4]
            df["covid"] = df['datetime'].between(date1, date2, inclusive=False)
            expander = st.expander("Table")
            expander.table(df)
            allDF = pd.concat([df, allDF], axis=0)
        except:
            st.write("YIKES")
    
csv = convert_df(allDF)

st.download_button(
     label="Download data as CSV",
     data=csv,
     file_name='large_df.csv',
     mime='text/csv',
 )
    
