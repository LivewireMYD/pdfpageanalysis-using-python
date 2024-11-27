import fitz  # PyMuPDF
from PIL import Image
import io
import os

def extract_images_and_check_dpi(pdf_path):
    pages_with_high_dpi = []  # Store pages with at least one image of 300 DPI or more
    
    try:
        # Open the PDF file
        doc = fitz.open(pdf_path)
        
        for page_num in range(len(doc)):  # Iterate over all pages
            page = doc.load_page(page_num)
            
            # Extract images from the page
            image_list = page.get_images(full=True)
            if image_list:
                """ print(f"Page {page_num + 1} contains images.") """
                page_has_high_dpi_image = False  # Flag to track if any image has 300 DPI
                
                for img_index, img in enumerate(image_list):
                    xref = img[0]  # Reference to the image
                    base_image = doc.extract_image(xref)
                    image_bytes = base_image["image"]  # Extract the image byte data
                    
                    # Load the image into PIL
                    image = Image.open(io.BytesIO(image_bytes))
                    width, height = image.size
                    dpi_x, dpi_y = image.info.get('dpi', (72, 72))  # Default DPI is 72 if not found

                    """ print(f"  Image {img_index + 1} resolution: {width}x{height} pixels")
                    print(f"  Image {img_index + 1} DPI: {dpi_x}x{dpi_y}") """
                    
                    if dpi_x < 300 and dpi_y < 300:
                        
                        page_has_high_dpi_image = True  # Mark this page as having high-DPI image
                
                # If the page has any image with DPI >= 300, store the page number
                if page_has_high_dpi_image:
                    pages_with_high_dpi.append(page_num + 1)  # Store 1-based page number
                
            else:
                print(f"Page {page_num + 1} does not contain images.")
        
        return pages_with_high_dpi  # Return the list of pages with high-DPI images
    
    except Exception as e:
        print(f"Error checking PDF: {e}")
        return []

def check_all_pdfs_in_folder(folder_path):
    # Get all PDF files in the folder
    pdf_files = [f for f in os.listdir(folder_path) if f.endswith('.pdf')]
    
    for pdf_file in pdf_files:
        pdf_path = os.path.join(folder_path, pdf_file)
        """ print(f"Checking PDF file: {pdf_file}") """
        
        # Call the function to extract images and check DPI
        pages_with_high_dpi = extract_images_and_check_dpi(pdf_path)
        
        if pages_with_high_dpi:
            print(f"Pages with 300 DPI or higher images in {pdf_file}: {pages_with_high_dpi}")
        else:
            print(f"No pages with 300 DPI or higher images in {pdf_file}.")

# Example usage
folder_path = "samplepdf"  # Replace with your folder path
check_all_pdfs_in_folder(folder_path)
