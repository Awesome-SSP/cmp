import fitz  # PyMuPDF
import sys
import os

def compress_pdf(input_path, output_path, image_quality=30):
    # Open the original PDF
    pdf_document = fitz.open(input_path)
    
    # Create a new PDF for output
    new_pdf = fitz.open()

    for page_num in range(len(pdf_document)):
        page = pdf_document.load_page(page_num)
        pix = page.get_pixmap(dpi=150)  # Lower DPI to reduce size
        img = fitz.Pixmap(pix, 0) if pix.alpha else pix

        rect = page.rect
        new_page = new_pdf.new_page(width=rect.width, height=rect.height)
        new_page.insert_image(rect, pixmap=img, keep_proportion=True)

    # Save to output path
    new_pdf.save(output_path, deflate=True, garbage=4, clean=True)
    new_pdf.close()
    pdf_document.close()

    print(f"Compressed PDF saved to: {output_path}")

# Example usage
input_pdf = "Saurabh_07-1.pdf"
output_pdf = "Saurabh_07-2.pdf"
compress_pdf(input_pdf, output_pdf)
