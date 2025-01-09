import re
from datetime import datetime

from astrapy import DataAPIClient

import streamlit as st
import json
import requests
import pandas as pd
from typing import Optional

# Constants
BASE_API_URL = "https://api.langflow.astra.datastax.com"
LANGFLOW_ID = "d880689d-9f1a-4dde-aab5-5631ac6f952e"
FLOW_ID = "e8c8c783-1f70-4e9b-91c7-6549f18b55e5"
ENDPOINT = "e8c8c783-1f70-4e9b-91c7-6549f18b55e5"

ASTRA_TOKEN = ""
db_api_endpoint = ""
collection_name = ""


def process_and_preview_file(uploaded_file):
    """Process uploaded file and show preview with statistics."""
    try:
        df = pd.read_csv(uploaded_file)

        st.subheader("File Preview")
        st.write(f"File name: {uploaded_file.name}")
        st.write(f"Data shape: {df.shape}")

        # Data preview in tabs
        tab1, tab2, tab3 = st.tabs(["Data Sample", "Statistics", "Missing Values"])

        with tab1:
            st.dataframe(df.head())

        with tab2:
            col1, col2 = st.columns(2)
            with col1:
                st.write("Numeric Columns:")
                st.write(df.select_dtypes(include=['number']).columns.tolist())
            with col2:
                st.write("Text Columns:")
                st.write(df.select_dtypes(include=['object']).columns.tolist())

            if len(df.select_dtypes(include=['number']).columns) > 0:
                st.write("Numeric Statistics:")
                st.dataframe(df.describe())

        with tab3:
            missing_data = df.isnull().sum()
            if missing_data.any():
                st.write(missing_data[missing_data > 0])
            else:
                st.write("No missing values found")

        return df

    except Exception as e:
        st.error(f"Error processing file: {str(e)}")
        return None


def run_chat_flow(
        message: str,
        application_token: Optional[str] = None,
        output_type: str = "chat"
) -> dict:
    """Run a flow with a given message."""
    api_url = f"{BASE_API_URL}/lf/{LANGFLOW_ID}/api/v1/run/{ENDPOINT}"

    payload = {
        "input_value": message,
        "output_type": output_type,
        "input_type": "chat",
    }
    headers = None
    if application_token:
        headers = {"Authorization": "Bearer " + application_token, "Content-Type": "application/json"}

    response = requests.post(api_url, json=payload, headers=headers)
    return response.json()


def chat_interface():
    """Chat interface function."""
    global ASTRA_TOKEN

    st.title("Chat Analyzer")

    with st.sidebar:
        st.header("Chat Configuration")
        ASTRA_TOKEN = st.text_input("Application Token", type="password")
        show_raw_response = st.checkbox("Show Raw Response", value=False)

    if not ASTRA_TOKEN:
        st.error("Application Token is required!")
        return

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("What's on your mind?"):
        with st.chat_message("user"):
            st.markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.spinner("Thinking..."):
            try:
                response = run_chat_flow(
                    message=prompt,
                    application_token=ASTRA_TOKEN
                )

                if show_raw_response:
                    with st.expander("Raw Response"):
                        st.json(response)

                if "outputs" in response:
                    assistant_message = response["outputs"][0]["outputs"][0]["results"]["message"]["data"]["text"]
                    with st.chat_message("assistant"):
                        st.markdown(assistant_message)
                    st.session_state.messages.append({"role": "assistant", "content": assistant_message})
                else:
                    st.error("No result found in the response")

            except Exception as e:
                st.error(f"Error: {str(e)}")

    if st.sidebar.button("Clear Chat"):
        st.session_state.messages = []
        st.rerun()


def process_and_convert_to_json(dataframe):
    dataframe = dataframe.fillna("")
    def map_age(age):
        try:
            age = int(age)
            if 4 <= age <= 12:
                return "Child"
            elif 13 <= age <= 19:
                return "Teenager"
            elif 20 <= age <= 24:
                return "Young adult"
            elif 40 <= age <= 59:
                return "Middle-aged people"
            elif age >= 60:
                return "Senior adult"
            else:
                return "Adult"
        except ValueError:
            return "Unknown"

    def map_time(time_str):
        time = datetime.strptime(time_str, "%H:%M:%S.%f").time()
        if time < datetime.strptime("07:00:00", "%H:%M:%S").time():
            return "early morning"
        elif time < datetime.strptime("12:00:00", "%H:%M:%S").time():
            return "morning"
        elif time < datetime.strptime("16:00:00", "%H:%M:%S").time():
            return "afternoon"
        elif time < datetime.strptime("20:00:00", "%H:%M:%S").time():
            return "evening"
        else:
            return "night"

    def process_description(description):
        age_match = re.search(r"\b(\d+) years old\b", description)
        age = map_age(age_match.group(1)) if age_match else "Unknown"

        time_match = re.search(r"(\d{2}:\d{2}:\d{2}\.\d+)", description)
        time_period = map_time(time_match.group(1)) if time_match else "Unknown"

        description = re.sub(r"\b\d+ years old\b", age, description)
        description = re.sub(r"\b\d{2}:\d{2}:\d{2}\.\d+\b", time_period, description)

        return description

    dataframe['description'] = dataframe['description'].apply(process_description)

    data = []
    for _, row in dataframe.iterrows():
        description = row.pop("description")
        metadata = row.to_dict()
        data.append({
            "$vectorize": description,
            "metadata": metadata
        })

    return json.dumps(data, indent=4)


def data_management():
    """Data management interface function."""
    global ASTRA_TOKEN, db_api_endpoint, collection_name

    st.title("Data Management")

    with st.sidebar:
        st.header("Database Configuration")
        db_api_endpoint = st.text_input("DB API Endpoint")
        collection_name = st.text_input("Collection Name")

    uploaded_file = st.file_uploader("Upload CSV File", type=['csv'])

    if uploaded_file is not None:
        df = process_and_preview_file(uploaded_file)

        if df is not None and st.button("Upload to Database"):
            if not ASTRA_TOKEN:
                st.error("Astra Token is required!")
                return

            if not db_api_endpoint:
                st.error("Database API Endpoint is required!")
                return

            if not collection_name:
                st.error("Collection Name is required!")
                return

            try:
                client = DataAPIClient(ASTRA_TOKEN)
                database = client.get_database(db_api_endpoint)
                collection = database[collection_name]

                json_data = process_and_convert_to_json(df)

                response = collection.insert_many(json.loads(json_data))

                if response:
                    st.success("Data successfully uploaded to the database!")
                    st.balloons()
                else:
                    st.error("Failed to upload data to the database")

            except Exception as e:
                st.error(f"Error uploading to database: {str(e)}")


def main():
    st.set_page_config(page_title="LangFlow Social Media Analyzer App", page_icon="🤖", layout="wide")
    st.header("LangFlow Social Media Analyzer App")

    tab1, tab2 = st.tabs(["💬 Analyzer", "📊 Add more data"])

    with tab1:
        chat_interface()

    with tab2:
        data_management()


if __name__ == "__main__":
    main()