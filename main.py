import fitz  # PyMuPDF
from PIL import Image
import pytesseract
import re

def extract_and_check_page_numbers(file_path):
    try:
        pdf_document = fitz.open(file_path)
        total_pages = pdf_document.page_count
        print(f"Total pages in PDF: {total_pages}")
        
        extracted_page_numbers = []
        
        for page_num in range(total_pages):
            page = pdf_document.load_page(page_num)
            pix = page.get_pixmap()  # Render page to an image
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

            # Use OCR to extract text from the image
            text = pytesseract.image_to_string(img)

            # Use regex to find page numbers in the text
            match = re.search(r'\b\d+\b', text)  # Look for standalone numbers (e.g., "1", "2", etc.)
            if match:
                page_number = int(match.group(0))
                extracted_page_numbers.append(page_number)
                print(f"Page {page_num + 1} contains page number: {page_number}")
            else:
                print(f"Page {page_num + 1} does not contain a page number.")
                extracted_page_numbers.append(None)  # Use `None` for pages without page numbers

        # Check if page numbers are sequential
        print("\nChecking page number sequence...")
        for idx, number in enumerate(extracted_page_numbers):
            if idx > 0 and number is not None and extracted_page_numbers[idx - 1] is not None:
                if number != extracted_page_numbers[idx - 1] + 1:
                    print(f"Non-sequential page numbers found between page {idx} and {idx + 1}: {extracted_page_numbers[idx - 1]} -> {number}")
        
        print("\nPage number extraction complete.")
    
    except Exception as e:
        print(f"Error: {e}")


# Replace with your PDF file path
file_path = 'samplepdf/5MdPRR_9780201134841_Analytic Geometry 7th Edition.pdf'  
extract_and_check_page_numbers(file_path)
