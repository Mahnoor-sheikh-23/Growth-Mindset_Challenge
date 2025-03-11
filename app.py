import streamlit as st
import pandas as pd
import os
import io
import matplotlib.pyplot as plt
import seaborn as sns

# Set up the app with better UI
st.set_page_config(page_title="💿 Data Sweeper", layout="wide")
st.title("💿 Data Sweeper")
st.markdown(
    "### 🚀 Transform your files between CSV and Excel formats with built-in data cleaning and visualization!"
)

# Sidebar for navigation
st.sidebar.header("📌 About Data Sweeper")
st.sidebar.info(
    "This app helps you clean, analyze, and convert CSV/Excel files effortlessly. "
    "Upload a file, clean the data, visualize insights, and download the transformed dataset!"
)

uploaded_files = st.file_uploader("📂 Upload your files (CSV or Excel)", type=["csv", "xlsx"], accept_multiple_files=True)

if uploaded_files:
    for file in uploaded_files:
        file_ext = os.path.splitext(file.name)[-1].lower()
        
        if file_ext == ".csv":
            df = pd.read_csv(file)
        elif file_ext == ".xlsx":
            df = pd.read_excel(file)
        else:
            st.error(f"Unsupported file type: {file_ext}")
            continue

        # File Details
        st.markdown(f"### 📄 File: `{file.name}`")
        st.write(f"📏 **File Size:** {file.size / 1024:.2f} KB")

        # Preview the data
        st.subheader("🔍 Data Preview")
        st.dataframe(df.head())

        # Data Cleaning Options
        st.subheader("🛠 Data Cleaning")
        col1, col2 = st.columns(2)
        
        with col1:
            if st.checkbox(f"✅ Remove duplicates ({file.name})"):
                df.drop_duplicates(inplace=True)
                st.success("Duplicates removed!")
        
        with col2:
            if st.button(f"🧹 Fill Missing Values ({file.name})"):
                numeric_cols = df.select_dtypes(include=["number"]).columns
                df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                st.success("Missing values filled with column means!")
        
        # Column Selection
        st.subheader("📌 Select Columns")
        columns = st.multiselect(f"Choose columns to keep ({file.name})", df.columns, default=df.columns)
        df = df[columns]
        
        # Data Visualization
        st.subheader("📊 Data Visualization")
        if st.checkbox(f"📈 Show Data Visualization ({file.name})"):
            numeric_cols = df.select_dtypes(include=["number"]).columns
            if len(numeric_cols) >= 2:
                fig, ax = plt.subplots(figsize=(8, 5))
                sns.barplot(x=df[numeric_cols[0]], y=df[numeric_cols[1]], ax=ax)
                ax.set_title("Feature Comparison")
                st.pyplot(fig)
            else:
                st.warning("Not enough numerical columns for visualization.")
        
        # File Conversion
        st.subheader("🔄 Convert File Format")
        conversion_type = st.radio(f"Convert `{file.name}` to:", ["CSV", "Excel"], key=file.name)
        
        if st.button(f"🚀 Convert {file.name}"):
            buffer = io.BytesIO()
            output_file_name = file.name.replace(file_ext, f".{conversion_type.lower()}")
            mime_type = "text/csv" if conversion_type == "CSV" else "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            
            if conversion_type == "CSV":
                df.to_csv(buffer, index=False)
            else:
                df.to_excel(buffer, index=False, engine="openpyxl")
            buffer.seek(0)
            
            st.download_button(
                label=f"⬇ Download {output_file_name}",
                data=buffer,
                file_name=output_file_name,
                mime=mime_type
            )

st.sidebar.success("🎉 Ready to clean and transform your data!")
