import os
import pandas as pd
import re
import streamlit as st

##Define Current Directory
'''
current_dir = os.path.dirname(os.path.abspath(__file__))

def get_dataset_path():
    csv_path = os.path.join(current_dir,"Data","customer_reviews.csv")
    return csv_path
'''

# Helper function to clean text
def clean_text(text):
    text = text.lower().strip()
    text = re.sub(r'[^\w\s]', '', text)
    return text

st.title("Welcome!")
st.write("This is an app project based on the rapid prototyping course from Deeplearning.AI")

#Layout two buttons side to side
col1, col2 =st.columns(2)

with col1:
    if st.button("Ingest Dataset"):
        try:
            #csv_path = get_dataset_path()
            #Streamlit runs the app from top to bottom everytime the user interacts. So all the variables are reset and context lost. To work on it continuously you need to add it to the session state
            #st.session_state["df"] = pd.read_csv(csv_path) ##Add the data frame to the session state (very very important)
            st.session_state["df"] = pd.read_csv("customer_reviews.csv")
            st.success("Dataset loaded successfully")
        except FileNotFoundError:
            st.error("Dataset not found. Please check file path")


with col2:
    if st.button("Parse Reviews"):
        if "df" in st.session_state:
            st.session_state["df"]["CLEANED_SUMMARY"] = st.session_state["df"]["SUMMARY"].apply(clean_text)
            st.success("Reviews parsed and cleaned!")
        else:
            st.warning("Please ingest the dataset first.")

# Display the dataset if it exists
if "df" in st.session_state:
    # Product filter dropdown
    st.subheader("🔍 Filter by Product")
    product = st.selectbox("Choose a product", ["All Products"] + list(st.session_state["df"]["PRODUCT"].unique()))
    
    st.subheader(f"📁 Reviews for {product}")

    if product != "All Products":
        filtered_df = st.session_state["df"][st.session_state["df"]["PRODUCT"] == product]
    else:
        filtered_df = st.session_state["df"]
    st.dataframe(filtered_df)

    st.subheader("Sentiment Score by Product")
    grouped = st.session_state["df"].groupby(["PRODUCT"])["SENTIMENT_SCORE"].mean()
    st.bar_chart(grouped)