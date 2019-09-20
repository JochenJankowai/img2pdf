import os
from fpdf import FPDF
import argparse
import glob
from PIL import Image
from colorama import init, Fore, Style
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument("path", type=str)
parser.add_argument("dpi", type=int)
args = parser.parse_args()

init()

images = glob.glob(args.path + '/**/*.png', recursive=True)
images += glob.glob(args.path + '/**/*.jpg', recursive=True)
images += glob.glob(args.path + '/**/*.jpeg', recursive=True)

num_images = len(images)

if num_images == 0:
    quit()

i = 0

print(Fore.CYAN + "____________________________________________________\n")
print(Style.BRIGHT + "Converting " + str(num_images) + " images to PDFs at a quality of " + str(args.dpi) + "DPI." + Style.NORMAL)
print("____________________________________________________\n")

for image in images:
    absolute_path = os.path.dirname(os.path.abspath(image))
    folder_name = os.path.split(absolute_path)[1]
    pdf_filename = os.path.splitext(os.path.basename(image))[0] + ".pdf"
    ps_filename = os.path.splitext(os.path.basename(image))[0] + ".ps"
    absolute_pdf_filename = absolute_path + '/' + pdf_filename
    absolute_ps_filename = absolute_path + '/' + ps_filename

    space = ((i+1) / 10) < 0.98

    print("Generating PDF file (" + (" " if space else "") + Fore.MAGENTA + Style.BRIGHT + str(i + 1) + Style.NORMAL
          + Fore.CYAN + "/" + Fore.MAGENTA + str(num_images) + Fore.CYAN + "): " + folder_name + "/" + pdf_filename)

    with Image.open(image) as img:
        width_px, height_px = img.size
        width_in = width_px/args.dpi
        height_in = height_px/args.dpi

        pdf = FPDF(unit='in', format=tuple((width_in,height_in)))
        pdf.add_page()
        pdf.image(image, 0, 0, width_in, height_in)

        pdf.output(absolute_pdf_filename, "F")

    i = i + 1

    # We need to convert the PDF to PS and back because of some meta data that is added by FPDF which Latex doesn't like
    subprocess.check_output(['pdf2ps', absolute_pdf_filename, absolute_ps_filename])

    subprocess.check_output(['ps2pdf', absolute_ps_filename, absolute_pdf_filename])

    subprocess.check_output(['rm', absolute_ps_filename ])


print(Style.RESET_ALL)
