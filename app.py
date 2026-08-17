import streamlit as st
import pdfplumber 
import cv2
import numpy as np
from PIL import Image
import openpyxl
import re
import io
import pandas as pd

def extract_pdftext(pdf_file):
    text = ""
    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            text += page.extract_text()
    return text

def parse_table(text):
    lines = text.split('\n')
    data = []
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
        
        line = re.sub(r'^(\d+(\s\d+)*)\s*\.', lambda m: m.group(0).replace(' ', ''), line)
        
        if re.match(r'^\d+\.', line):
            parts = re.split(r'\s+', line)
            if len(parts) >= 10:
                sn = parts[0]
                qty = parts[1]
                amount = parts[-1]
                cgst = parts[-2]
                sgst = parts[-3]
                dis = parts[-4]
                scheme = parts[-5]
                rate = parts[-6]
                hsn = parts[-7]
                mrp = parts[-8]
                
                product_and_pack = parts[2:-8]
                product = ' '.join(product_and_pack[:-1])
                pack = product_and_pack[-1] if product_and_pack else ''
                
                data.append([sn, qty, product, pack, mrp, hsn, rate, scheme, dis, sgst, cgst, amount])
    
    return data

def create_excel(data):
    wb = openpyxl.Workbook()
    ws = wb.active

    headers = ['Sn', 'Qty', 'Product', 'Pack', 'EXP', 'MRP', 'HSN', 'Scheme', 'Dis%', 'SGST', 'CGST', 'Amount']
    ws.append(headers)

    for row in data:
        ws.append(row)

    output = io.BytesIO() #save file in mem not disk
    wb.save(output)
    output.seek(0) 
    return output

def show_editable_table(data):
    headers = ['Sn', 'Qty', 'Product', 'Pack', 'EXP', 'MRP', 'HSN', 'Scheme', 'Dis%', 'SGST', 'CGST', 'Amount']
    df = pd.DataFrame(data, columns=headers)
    edited_df = st.data_editor(df, num_rows="dynamic", use_container_width=True)
    return edited_df.values.tolist()

#UI
st.title("MedChem Pharmaceuticals")
st.write("Bill Data Extractor")
st.write("Upload an PDF or image of the bill and download it as an Excel file.")

uploaded_file = st.file_uploader("Upload Bill", type=["pdf", "jpg", "jpeg", "png"])

if uploaded_file is not None:
    file_type = uploaded_file.name.split('.')[-1].lower()

    if st.button("Extract Data"):
        with st.spinner("*please wait*"):
            if file_type == "pdf":
                text = extract_pdftext(uploaded_file)
                st.text(text)
            else:
                st.error("soon")
                st.stop()
            
            data = parse_table(text)

            if len(data) == 0:
                st.error("No data found.")
            else:
                st.success(f"Found {len(data)} rows")
                editable_data = show_editable_table(data)
                excel_file = create_excel(editable_data)
                st.download_button(
                    label = "Download Excel File",
                    data = excel_file,
                    file_name = "bill_data.xlsx",
                    mime = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
                