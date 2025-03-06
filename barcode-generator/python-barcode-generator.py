import barcode
from barcode.writer import ImageWriter
from fpdf import FPDF
import os

os.chdir(os.path.dirname(__file__))

# Read data from file
with open("barcode_input.txt", "r") as file:
    data = file.read().splitlines()

# Remove duplicates while preserving order
unique_data = list(dict.fromkeys(filter(None, data)))

# Directory for temporary barcode images
temp_dir = "temp_barcodes"
os.makedirs(temp_dir, exist_ok=True)

# Cleanup previous barcodes
for file in os.listdir(temp_dir):
    os.remove(os.path.join(temp_dir, file))

# Generate barcodes and save as images
barcode_files = []
for item in unique_data:
    code128 = barcode.get_barcode_class('code128')
    barcode_obj = code128(item, writer=ImageWriter())
    file_path = os.path.join(temp_dir, f"{item.strip().replace(' ', '_')}")  # Keep original case
    barcode_obj.save(file_path)
    barcode_files.append(file_path)

# Create a PDF with one barcode per page
pdf = FPDF()
for item in unique_data:
    file_path = os.path.join(temp_dir, f"{item.strip().replace(' ', '_')}.png")  # Use original case
    pdf.add_page()
    pdf.image(file_path, x=30, y=50, w=150)  # Centered barcode

# Save PDF
output_pdf = "barcodes.pdf"
pdf.output(output_pdf)

# Cleanup temporary images
for file in os.listdir(temp_dir):
    os.remove(os.path.join(temp_dir, file))
os.rmdir(temp_dir)

print(f"Barcode PDF generated: {output_pdf}")