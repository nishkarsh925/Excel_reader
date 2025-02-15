import streamlit as st
import google.generativeai as genai
import pandas as pd
import tempfile

# Set up Google Gemini API
GOOGLE_API_KEY = "AIzaSyBaz6Ly4_dBvjHmeDDJZU7mtbF3oI9t1us"  # Replace with your actual API key
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel("gemini-pro")

# Streamlit UI
st.title("📊 AI-Powered Excel Q&A App")

# File Upload
uploaded_file = st.file_uploader("Upload your Excel file", type=["xlsx", "xls"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    st.success(f"Uploaded: {uploaded_file.name}")
    st.dataframe(df.head())  # Show first few rows

    # Question Input
    question = st.text_input("Ask a question about your data:")
    if st.button("Get Answer"):
        if question:
            result = df[df.apply(lambda row: question.lower() in row.astype(str).str.lower().to_string(), axis=1)]
            if not result.empty:
                st.write("🔍 Found matching records:")
                st.dataframe(result)
            else:
                prompt = f"Here is a dataset:\n\n{df.head().to_string(index=False)}\n\nQuestion: {question}\nAnswer based on this data:"
                response = model.generate_content(prompt)
                st.write("🤖 AI Answer:", response.text)

    # Filtering & Download
    query = st.text_input("Filter data by keyword:")
    if st.button("Download Filtered Data"):
        filtered_data = df[df.apply(lambda row: query.lower() in row.astype(str).str.lower().to_string(), axis=1)]
        if not filtered_data.empty:
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx")
            filtered_data.to_excel(temp_file.name, index=False)
            st.success("Filtered file ready!")
            st.download_button("📥 Download Excel File", temp_file.name)
        else:
            st.error("No matching records found!")
