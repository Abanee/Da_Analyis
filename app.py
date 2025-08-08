import streamlit as st
from rag_pipeline import RAGPipeline
from data_parser import parse_file
from analytics import analyze_data
from export_visuals import export_to_powerbi, export_to_tableau
import os

st.title("RAG Data Analytics Platform")
st.write("Upload your data file (Excel, CSV, or PDF) to analyze and generate insights.")

# File upload
uploaded_file = st.file_uploader("Choose a file", type=["csv", "xlsx", "pdf"])
if uploaded_file:
    # Save uploaded file
    os.makedirs("data", exist_ok=True)
    file_path = f"data/{uploaded_file.name}"
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    # Parse file
    try:
        df, text = parse_file(file_path)
        st.write("Parsed Data Preview:")
        st.dataframe(df.head())

        # Analyze data
        insights = analyze_data(df)
        st.write("Data Insights:")
        for insight in insights:
            st.write(f"- {insight}")

        # Initialize RAG pipeline
        rag = RAGPipeline()
        rag.load_data(df, text)

        # User query
        query = st.text_input("Ask a question about your data:")
        if query:
            response = rag.query(query)
            st.write("RAG Response:", response)

        # Export options
        export_format = st.selectbox("Choose export format:", ["None", "PowerBI", "Tableau"])
        if export_format != "None" and st.button("Export"):
            os.makedirs("output", exist_ok=True)
            output_path = f"output/{uploaded_file.name.split('.')[0]}_{export_format.lower()}"
            if export_format == "PowerBI":
                export_to_powerbi(df, output_path + ".csv")
                st.success(f"Exported to {output_path}.csv for PowerBI")
            elif export_format == "Tableau":
                export_to_tableau(df, output_path + ".hyper")
                st.success(f"Exported to {output_path}.hyper for Tableau")
    except Exception as e:
        st.error(f"Error processing file: {str(e)}")
