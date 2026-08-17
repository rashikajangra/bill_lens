# Bill Lens

BillLens is a lightweight **bill/invoice data extraction tool** built with Python and Streamlit. It extracts tabular data from PDF bills, displays the extracted records in an editable table, and allows users to export the corrected data as an Excel file.

The project was designed to reduce the manual effort involved in transferring bill data from PDF documents into spreadsheets.

## Features

* Upload PDF bills through a web interface
* Extract text from PDF files using `pdfplumber`
* Parse product and billing information from extracted text
* Display extracted records in an editable table
* Add, remove, or modify rows before export
* Export processed data as an `.xlsx` Excel file
* In-memory Excel generation without creating temporary files on disk
* Simple Streamlit-based user interface

## Tech Stack

| Technology | Purpose                   |
| ---------- | ------------------------- |
| Python     | Core application logic    |
| Streamlit  | Web interface             |
| pdfplumber | PDF text extraction       |
| Pandas     | Tabular data manipulation |
| OpenPyXL   | Excel file generation     |
| Regex      | Bill text parsing         |
| NumPy      | Data processing support   |
| OpenCV     | Image-processing support  |
| Pillow     | Image handling            |

## How It Works

```text
             ┌─────────────────┐
             │   Upload Bill   │
             │      (PDF)      │
             └────────┬────────┘
                      │
                      ▼
             ┌─────────────────┐
             │ PDF Text        │
             │ Extraction      │
             │ pdfplumber      │
             └────────┬────────┘
                      │
                      ▼
             ┌─────────────────┐
             │ Table Parsing   │
             │ Regex + Python  │
             └────────┬────────┘
                      │
                      ▼
             ┌─────────────────┐
             │ Editable Data   │
             │ Table (Pandas)  │
             └────────┬────────┘
                      │
                      ▼
             ┌─────────────────┐
             │ Excel Generation│
             │    OpenPyXL     │
             └────────┬────────┘
                      │
                      ▼
             ┌─────────────────┐
             │ Download .xlsx  │
             └─────────────────┘
```

## Extracted Fields

The parser is currently designed to extract fields such as:

* Serial Number
* Quantity
* Product
* Pack
* MRP
* HSN
* Rate
* Scheme
* Discount
* SGST
* CGST
* Amount

The extracted records can be edited before generating the final Excel file.

## Project Structure

```text
BillFlow/
│
├── app.py
├── requirements.txt
├── README.md
└── ...
```

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/your-username/billflow.git
cd billflow
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

On macOS/Linux:

```bash
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the application

```bash
streamlit run app.py
```

The application will open in your browser.

## Usage

1. Upload a supported PDF bill.
2. Click **Extract Data**.
3. BillFlow extracts the text from the PDF.
4. The parser identifies product rows and billing fields.
5. Review and edit the extracted data in the interactive table.
6. Click **Download Excel File**.
7. Save the generated `.xlsx` file for further processing.

## Current Limitations

The current version has some format-specific limitations:

* PDF extraction is currently supported.
* Image-based bill extraction is not implemented yet.
* The table parser relies on the structure and ordering of fields in the input bill.
* Bills with significantly different layouts may require modifications to the parsing logic.
* OCR is not currently integrated into the extraction pipeline.

## Future Improvements

Planned improvements include:

* Add OCR support for scanned/image-based bills
* Use OpenCV for image preprocessing
* Support multiple bill and invoice formats
* Improve table detection and parsing
* Automatically detect column positions
* Add validation for extracted values
* Improve error handling for malformed PDFs
* Support additional export formats
* Add automated tests for different bill layouts
* Deploy the application for online use

## Key Implementation Details

### PDF Extraction

`pdfplumber` is used to extract text from each page of the uploaded PDF.

```python
with pdfplumber.open(pdf_file) as pdf:
    for page in pdf.pages:
        text += page.extract_text()
```

### Table Parsing

Regular expressions and string processing are used to identify product rows and separate fields such as quantity, product name, MRP, HSN, taxes, and amount.

### Editable Data

The extracted data is converted into a Pandas DataFrame and displayed using Streamlit's interactive data editor. This allows users to correct extraction errors before exporting the final spreadsheet.

### Excel Export

OpenPyXL is used to generate the Excel workbook. The workbook is created in memory using `BytesIO`, allowing the user to download the generated file directly without creating an intermediate file on disk.

## Example Workflow

**Input:**

```text
PDF Bill
   ↓
Text Extraction
   ↓
Product/Table Parsing
   ↓
Editable Records
   ↓
Excel Export
```

**Output:**

```text
bill_data.xlsx
```

## Why This Project?

Manual entry of billing information into spreadsheets can be repetitive and error-prone. BillFlow demonstrates how document processing, structured text parsing, data manipulation, and file generation can be combined into a simple automation workflow.

## License

This project is available for educational and personal use. Add an appropriate license file if you intend to distribute or modify the project publicly.
