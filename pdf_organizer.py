from PyPDF2 import PdfReader, PdfWriter
import os

def reorganize_pdf(input_path, output_path, page_order):
    """
    Reorganize pages in a PDF according to the specified order.
    
    Args:
        input_path (str): Path to the input PDF file
        output_path (str): Path to save the reorganized PDF
        page_order (list): List of page numbers (0-indexed) in the desired order
    """
    # Create PDF reader and writer objects
    reader = PdfReader(input_path)
    writer = PdfWriter()
    
    # Validate page order
    total_pages = len(reader.pages)
    for page_num in page_order:
        if page_num >= total_pages:
            raise ValueError(f"Page number {page_num} is out of range (max {total_pages-1})")
    
    # Add pages in the specified order
    for page_num in page_order:
        writer.add_page(reader.pages[page_num])
    
    # Write the output file
    with open(output_path, 'wb') as output_file:
        writer.write(output_file)
    
    print(f"Reorganized PDF saved to: {output_path}")

def main():
    # Input file path
    input_pdf = "./ballot0001.pdf"
    
    # Verify file exists
    if not os.path.exists(input_pdf):
        print("Error: The specified file does not exist.")
        return
    
    order_input = [0,1,2,4,6,8,10,12,11,9,7,5,3]
    
    try:
        page_order = [num for num in order_input]
    except ValueError:
        print("Error: Please enter only numbers separated by commas.")
        return
    
    # Verify we have all 13 pages
    if len(page_order) != 13:
        print(f"Error: You specified {len(page_order)} pages, but the PDF has 13 pages.")
        return
    
    # Output file path
    output_pdf = os.path.splitext(input_pdf)[0] + "_reorganized.pdf"
    
    # Reorganize the PDF
    try:
        reorganize_pdf(input_pdf, output_pdf, page_order)
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()