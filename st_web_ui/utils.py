import io
import os
import plotly.graph_objects as go
import plotly.io as pio
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


# Function to save Plotly plot as image
def save_plot_as_image(fig, filename):
    pio.kaleido.scope.default_width = 800  # set the resolution of the image
    fig.write_image(filename)

# Function to create a PDF from image files
def create_pdf(image_files, output_pdf):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    for image_file in image_files:
        c.drawImage(image_file, 0, height-500, width=width, height=400)  # Adjust image size and position
        c.showPage()  # Add a new page

    c.save()
    buffer.seek(0)  # Move the pointer to the beginning of the buffer
    return buffer

# Function to generate the PDF and allow download
def generate_pdf_and_download(plots):
    image_files = []
    for i, fig in enumerate(plots):
        image_filename = f"plot_{i}.png"
        save_plot_as_image(fig, image_filename)
        image_files.append(image_filename)

    # Create PDF and return it as a binary stream
    pdf_buffer = create_pdf(image_files, "plots.pdf")

    # Clean up the image files
    for image_file in image_files:
        os.remove(image_file)

    return pdf_buffer

def generate_pdf(plots):
    image_files = []
    for i, fig in enumerate(plots):
        image_filename = f"plot_{i}.png"
        save_plot_as_image(fig, image_filename)
        image_files.append(image_filename)

    create_pdf(image_files, "plots.pdf")

    for image_file in image_files:
        os.remove(image_file)
