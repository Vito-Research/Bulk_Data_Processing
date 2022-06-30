import streamlit as st
import pandas as pd
import os
import datetime
import json
import requests
import numpy as np
def convert_df(df):
     # IMPORTANT: Cache the conversion to prevent computation on every rerun
     return df.to_csv().encode('utf-8')

def averageForDay(df):
   
    return df.groupby(pd.Grouper(key="datetime", freq="d"))["heartrate", "datetime", "covid"].mean()
uploaded_file = st.file_uploader("Choose a file")
allDF = pd.DataFrame()
if uploaded_file is not None:
    dfUploaded = pd.read_csv(uploaded_file)
    for index, row in dfUploaded.iterrows():
        if index == 1:
            rowID = row["Participant ID"]
        
            df = pd.DataFrame()
            try:
                df = pd.read_csv(("./COVID-19-Phase2-Wearables-2/" + rowID + "/Orig_Fitbit_HR.csv"))

            except:
                try:
                    df = pd.read_csv(("./COVID-19-Phase2-Wearables-2/" + rowID + "/Orig_NonFitbit_HR.csv"))
                except:
                    st.write(("./COVID-19-Phase2-Wearables-2/" + rowID + "/Orig_Fitbit_HR.csv"))
           
            row["COVID-19 Test Date"] = pd.to_datetime(row["COVID-19 Test Date"])
            df["datetime"] = pd.to_datetime(df["datetime"])
            df = df[df["datetime"].dt.hour < 4]
            date1 = pd.to_datetime(row["COVID-19 Test Date"] + datetime.timedelta(days=-3))
            date2 = pd.to_datetime(row["COVID-19 Test Date"] + datetime.timedelta(days=3))
           
            
            df["covid"] = df["datetime"].between(date1, date2, inclusive=True)
            # df["covid"] = (1 if df["covid"] == True else 0)
            # covidArr = True if date1 >= pd.to_datetime(df["datetime"]) else False
            
            # df["covid"] = covidArr

            df = averageForDay(df)
            st.table(df)
            withinMonthOfAlert = row["COVID-19 Test Date"] + datetime.timedelta(days=-30)
            withinMonthOfAlert2 = row["COVID-19 Test Date"] + datetime.timedelta(days=10)
            
            
            df.index = pd.to_datetime(df.index)
            # df["covid"] = (True if ((df.index >= date1),  (df.index <= date2)) else False)
            
            expander = st.expander("Table")
            
            expander.write(df)
           # allDF = pd.concat([df, allDF], axis=0)

            url = "https://testingcer.herokuapp.com/"
            jsonData = {}
            st.write(df)
            
            jsonData["arr"] = df["heartrate"].tolist()
            st.text(json.dumps(jsonData))
            r = requests.post(url, json=jsonData)
            listOfAlerts = r.text.strip('][').split(',')
            df = df.reset_index()
            compareDf = df
            compareDf["predicted"] = pd.Series(listOfAlerts)
            
            st.table(compareDf)
          
    
csv = convert_df(allDF)

st.download_button(
     label="Download data as CSV",
     data=csv,
     file_name='large_df.csv',
     mime='text/csv',
 )
    
