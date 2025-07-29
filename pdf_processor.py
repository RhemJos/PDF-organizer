from PyPDF2 import PdfReader, PdfWriter
import os

class PDFProcessor:
    """PDF processor to reorganize and crop pages of a PDF."""
    def __init__(self):
        self.order_pages = [0,1,2,4,6,8,10,12,11,9,7,5,3]
        self.crop_points_top = 54
        self.crop_points_bottom = 39

    def reorganize_pdf_pages(self, input_path, output_path, page_order):
        """
        Reorganize pages in a PDF according to the specified order.
        
        Args:
            input_path (str): Path to the input PDF file
            output_path (str): Path to save the reorganized PDF
            page_order (list): List of page numbers (0-indexed) in the desired order
        """
        reader = PdfReader(input_path)
        writer = PdfWriter()

        # Validate page order
        total_pages = len(reader.pages)
        for page_num in page_order:
            if page_num >= total_pages:
                raise ValueError(f"Page number {page_num} is out of range (max {total_pages-1})")
            
        # Add pages in the specified order
        for page_num in page_order:
            page = reader.pages[page_num]
            self.crop_page(page = page, crop_top_points=self.crop_points_top, crop_bottom_points=self.crop_points_bottom)
            writer.add_page(reader.pages[page_num])
        
        # Write the output file
        with open(output_path, 'wb') as output_file:
            writer.write(output_file)    
        print(f"Reorganized PDF saved to: {output_path}")

    def crop_page(self, page, crop_top_points=36, crop_bottom_points=36):
        """
        Crop a page. I takes crop values (in points, where 1 inch = 72 points)

        Args:
            page: the page object to be cropped. 
            crop_top_points (int): the amount of points to crop from the top of the page.
            crop_bottom_points (int): the amount of points to crop from the bottom of the page.
        """
        page.mediabox.upper_right =  (page.mediabox.right, page.mediabox.top - crop_top_points)
        page.mediabox.lower_left = (page.mediabox.left, page.mediabox.bottom + crop_bottom_points)

    def process_PDFs(self, input_path, output_path):
        """
        Process all PDFs from a given path and save them in a output path.

        Args:
            input_path (str): The path where all pdfs are saved.
            output_path (str): The path where all processed pdfs will be saved.
        """
        for root, _, files in os.walk(input_path):
            relative_path = os.path.relpath(root, input_path)
            for file in files:
                if file.endswith('.pdf'):
                    dest_folder_path = os.path.join(output_path, relative_path)
                    os.makedirs(dest_folder_path, exist_ok=True)
                    input_file_path = os.path.join(root, file)
                    output_file_path = os.path.join(dest_folder_path, file)
                    print(f"Processing {input_file_path}...")
                    self.reorganize_pdf_pages(input_file_path, output_file_path, self.order_pages)
                    print(f"Successfully. Saved to {output_file_path}")


if __name__ == "__main__":
    pdf = PDFProcessor()
    # pdf.process_PDFs(input_path='J:\\OBSCD\\Boletas Libros\\bucket\\test', output_path='J:\\OBSCD\\pruebas de renombrado')
    pdf.process_PDFs(input_path='J:\\OBSCD\\bucket\\d20', output_path='J:\\OBSCD\\pruebas de renombrado')
