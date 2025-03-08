import streamlit as st
import pandas as pd
from io import BytesIO

st.set_page_config(page_title="File Converter", layout="wide")
st.title("File Converter & cleaner")
st.write("upload a file and convert it to a different format")

files = st.file_uploader("Upload a file", type=["csv","pdf", "xlsx", "json", "txt"], accept_multiple_files=True)

if files : 
    for file in files : 
        ext = file.name.split(".")[-1]
        df = pd.read_csv(file) if ext == "csv" else pd.read_excel(file)

        st.subheader(f"{file.name} - preview")
        st.dataframe(df.head())

        if st.checkbox(f"remove dupliates - {file.name}"):
            df = df.drop_duplicates()
            st.success("dupliates removed")
            st.dataframe(df.head())

            if st.checkbox(f"Fill Missing Values - {file.name}"):
                df = fileno(df.select_dtypes(include=["number"]).mean(), inplace=True)
                st.success("missing values filled with mean")
                st.dataframe(df.head())

            selected_columns = st.multiselect(f"slect columns - {file.name}", df.columns, default=df.columns)    
            df = df[selected_columns]
            st.dataframe(df.head())


            if st.checkbox(f"show chart - {file.name}") and not df.select_dtypes(include="number").empty():
                st.bar_chart(df.select_dtypes(include="number").iloc[:,:2])

            format_choise = st.radio(f"convert {file.name} to:", ["csv", "Excel"], key=file.name)

            if st.button(f"Download {file.name} as {format_choise}"):
                output = BytesIO()
                if format_choise == "csv":
                    df.to_csv(output, index=False)
                    mine = "text/csv"
                    new_name = file.name.replace(ext, "csv")

                else:
                    df.to_excel(output, index=False , engine="openpyxl")
                    mine = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    new_name = file.name.replace(ext, "xlsx")

                output.seek(0)
                st.download_button("Download File", file_name = new_name, data = output, mime=mine)

            st.success("Process completed")

                    



