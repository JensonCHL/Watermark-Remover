# [ Welcome to Python PDF PROCESSOR ]
# [ Combined PDF Decrypter and Watermark Remover ]

import PyPDF2
from PyPDF4 import PdfFileReader as PyPDF4Reader, PdfFileWriter as PyPDF4Writer
from PyPDF4.pdf import ContentStream
from PyPDF4.generic import TextStringObject, NameObject
from PyPDF4.utils import b_
import os
import time


def decrypt_and_extract_all_pages(input_path, output_path):
    """
    Decrypt an encrypted PDF and save as a new unencrypted PDF using PyPDF2
    """
    try:
        # Try to open the PDF
        reader = PyPDF2.PdfReader(input_path)

        # Check if the PDF is encrypted
        if reader.is_encrypted:
            print(f"PDF {os.path.basename(input_path)} is encrypted. Attempting to decrypt...")
            # Try decrypting with empty password
            if reader.decrypt(''):
                print("Decrypted with empty password")
            else:
                print("Could not decrypt with empty password")
                # Try with common passwords
                common_passwords = ['']
                decrypted = False
                for pwd in common_passwords:
                    if reader.decrypt(pwd):
                        print(f"Decrypted with password: '{pwd}'")
                        decrypted = True
                        break
                if not decrypted:
                    print("Could not decrypt with common passwords")
                    return False

        # Create writer object
        writer = PyPDF2.PdfWriter()

        # Extract all pages
        num_pages = len(reader.pages)
        print(f"PDF has {num_pages} pages. Extracting all pages...")

        for i in range(num_pages):
            page = reader.pages[i]
            writer.add_page(page)
            print(f"Added page {i + 1}")

        # Save the extracted pages to a new PDF
        with open(output_path, 'wb') as output_file:
            writer.write(output_file)

        print(f"All {num_pages} pages extracted successfully to {os.path.basename(output_path)}")
        return True

    except Exception as e:
        print(f"Error extracting pages: {str(e)}")
        return False


def remove_watermark(wmText, inputFile, outputFile):
    """
    Remove watermark text from a PDF file
    """
    # This Function Reads PDF file and Removes the WATERMARK TEXT

    with open(inputFile, "rb") as f:
        source = PyPDF4Reader(f, "rb")
        output = PyPDF4Writer()

        for page in range(source.getNumPages()):
            page = source.getPage(page)
            content_object = page["/Contents"].getObject()
            content = ContentStream(content_object, source)

            for operands, operator in content.operations:
                if operator == b_("Tj"):
                    text = operands[0]

                    # Only process if we have watermark text to remove
                    if wmText:
                        for i in wmText:
                            if isinstance(text, str) and text.startswith(i):
                                operands[0] = TextStringObject('')

            page.__setitem__(NameObject('/Contents'), content)
            output.addPage(page)

        with open(outputFile, "wb") as outputStream:
            output.write(outputStream)


def watermark_text(inputFile, waterMarkTextStarting):
    """
    Read the PDF file and search for watermark text
    """
    # This Function reads the PDF file and searches for input string and deletes the WaterMark

    wmText = []
    pdfFileObj = open(inputFile, 'rb')
    pdfReader = PyPDF4Reader(pdfFileObj)
    pageObj = pdfReader.getPage(0)
    watermark = pageObj.extractText()
    pdfFileObj.close()

    # Check if the watermark text exists
    x = watermark.find(waterMarkTextStarting)
    if x == -1:
        print(f"  No watermark found starting with '{waterMarkTextStarting}'")
        return []  # Return empty list if watermark not found

    lengthWmText = len(waterMarkTextStarting)
    wmText.append(watermark[x:x+lengthWmText])
    wmText.append(watermark[x+lengthWmText:])
    return wmText


def draw():
    """
    Print welcome message
    """
    # This Function Prints the below message

    print(f'-'*57)
    print("|\t\tPYTHON PDF PROCESSOR\t\t\t|")
    print(f'-'*57)
    print("""[ Welcome to PYTHON PDF PROCESSOR ]""")
    print(f'-'*57)


def check_files_in_folder(dirName):
    """
    Check if any PDF files are present in the folder
    """
    # This Function is used to check if any pdf present in folder
    # if present executes next step
    # else prompts user to add pdf files to folder

    print(f"Checking for PDF files in '{dirName}' Folder...")
    print(f"-"*50)

    inputFilesNames = os.listdir(dirName)
    # Filter only PDF files
    inputFilesNames = [f for f in inputFilesNames if f.lower().endswith('.pdf')]
    if len(inputFilesNames) == 0:
        print(f"No PDF files Found in '{dirName}' Folder!")
        return []

    print(f"Total Number of PDF Files Found: {len(inputFilesNames)}")
    return inputFilesNames


def process_files(input_dir, output_dir, watermark_text_starting):
    """
    Process all PDF files in the input directory
    """
    print(f'-'*50)

    # Get list of PDF files
    input_files = check_files_in_folder(input_dir)

    # Check if there are any files to process
    if not input_files:
        print("No PDF files to process. Exiting.")
        return

    # First, decrypt all encrypted files
    print("\nStep 1: Decrypting encrypted files...")
    files_to_replace = []

    for idx, filename in enumerate(input_files):
        input_path = os.path.join(input_dir, filename)
        temp_decrypted_path = os.path.join(input_dir, f"temp_{filename}")

        print(f"Checking file {idx+1}/{len(input_files)}: {filename}")

        # Try to decrypt the file
        try:
            reader = PyPDF2.PdfReader(input_path)
            print(f"  File {filename} has {len(reader.pages)} pages.")
            if reader.is_encrypted:
                print(f"  File {filename} is encrypted. Decrypting...")
                success = decrypt_and_extract_all_pages(input_path, temp_decrypted_path)
                if success:
                    # Mark this file for replacement after we close all file handles
                    files_to_replace.append((input_path, temp_decrypted_path, filename))
                    print(f"  Marked {filename} for replacement with decrypted version.")
                else:
                    print(f"  Failed to decrypt {filename}.")
                    # Clean up temp file if it exists
                    if os.path.exists(temp_decrypted_path):
                        os.remove(temp_decrypted_path)
            else:
                print(f"  File {filename} is not encrypted. Skipping decryption.")
        except Exception as e:
            print(f"  Error checking encryption status for {filename}: {str(e)}")
            # Clean up temp file if it exists
            if os.path.exists(temp_decrypted_path):
                os.remove(temp_decrypted_path)

    # Now replace all marked files
    print("\nReplacing encrypted files with decrypted versions...")
    for original_path, temp_path, filename in files_to_replace:
        try:
            if os.path.exists(temp_path):
                os.replace(temp_path, original_path)  # os.replace is atomic
                print(f"  Replaced {filename} with decrypted version.")
            else:
                print(f"  Warning: Temp file for {filename} not found.")
        except Exception as e:
            print(f"  Error replacing {filename}: {str(e)}")
            # Clean up temp file if it exists
            if os.path.exists(temp_path):
                os.remove(temp_path)

    # Refresh the file list after decryption
    input_files = check_files_in_folder(input_dir)

    # Check again if there are files after decryption
    if not input_files:
        print("No PDF files to process after decryption. Exiting.")
        return

    # Then, remove watermarks from all files
    print("\nStep 2: Removing watermarks from files...")
    for idx, filename in enumerate(input_files):
        input_path = os.path.join(input_dir, filename)
        output_path = os.path.join(output_dir, filename)

        print(f"Processing file {idx+1}/{len(input_files)}: {filename}")

        try:
            wm_text = watermark_text(input_path, watermark_text_starting)
            if wm_text:
                remove_watermark(wm_text, input_path, output_path)
                print(f'  [ DONE ]  Watermark removed from {filename}')
            else:
                # Copy the file as-is to output if no watermark found
                with open(input_path, 'rb') as src, open(output_path, 'wb') as dst:
                    dst.write(src.read())
                print(f'  [ DONE ]  File copied to output (no watermark found)')
        except Exception as e:
            print(f"  Error processing {filename}: {str(e)}")
            # Copy the file as-is to output if processing fails
            try:
                with open(input_path, 'rb') as src, open(output_path, 'wb') as dst:
                    dst.write(src.read())
                print(f'  [ DONE ]  File copied to output (processing error)')
            except Exception as copy_error:
                print(f"  Error copying file: {str(copy_error)}")


def main():
    """
    Main function to run the PDF processor
    """
    # Driver Function

    draw()

    # Configuration
    input_dir = "Original Document"
    output_dir = "Result"

    # Prompt user for watermark text
    while True:
        watermark_text_starting = input("Enter the starting text of the watermark to remove: ").strip()
        if watermark_text_starting:
            break
        print("Watermark text cannot be empty. Please enter a value.")

    print(f"Using watermark text: {watermark_text_starting}")
    print(f"Input directory: {input_dir}")
    print(f"Output directory: {output_dir}")
    print(f'-'*50)

    # Check if input directory exists
    if not os.path.exists(input_dir):
        print(f"Error: Input directory '{input_dir}' does not exist!")
        return

    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Process all files
    process_files(input_dir, output_dir, watermark_text_starting)

    print(f'-'*50)
    print("Processing complete. Exiting...")


if __name__ == "__main__":
    main()