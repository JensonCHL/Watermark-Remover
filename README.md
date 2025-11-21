# PDF Processor - Decrypt and Remove Watermarks

A Python tool that automatically decrypts encrypted PDF files and removes watermarks from PDF documents in batch.

## Features

- **Automatic PDF Decryption**: Detects and decrypts encrypted PDF files using common passwords
- **Watermark Removal**: Removes text-based watermarks from PDF documents
- **Batch Processing**: Processes multiple PDF files in a single run
- **User-Friendly**: Simple interface with clear progress updates
- **Safe Processing**: Preserves original files and creates clean copies in a separate folder

## Prerequisites

- Python 3.x
- PyPDF2
- PyPDF4

## Installation

1. Clone or download this repository
2. Install the required packages:
   ```bash
   pip install PyPDF2 PyPDF4
   ```

## Usage

1. Place your PDF files (encrypted or unencrypted) in the `Original Document` folder
2. Run the script:
   ```bash
   python pdf_processor.py
   ```
3. When prompted, enter the starting text of the watermark you want to remove
4. Find your processed files in the `Result` folder

## How It Works

The script performs two main operations:

1. **Decryption Phase**:
   - Scans all PDF files in the `Original Document` folder
   - Detects encrypted files automatically
   - Attempts to decrypt using common passwords:
     - Empty password
   - Replaces encrypted files with decrypted versions

2. **Watermark Removal Phase**:
   - Processes all PDF files in the folder
   - Searches for watermarks that start with the user-specified text
   - Removes matching watermark text from the documents
   - Saves cleaned versions to the `Result` folder

## Folder Structure

```
PDF Processor/
├── pdf_processor.py          # Main script
├── Original Document/        # Input folder for PDF files
├── Result/                   # Output folder for processed files
└── README.md                 # This file
```

## Notes

- The script preserves the original filenames in the output
- If no watermark is found matching the specified text, the file is copied unchanged
- If decryption fails, the file is processed as-is
- The script handles errors gracefully and continues processing other files
