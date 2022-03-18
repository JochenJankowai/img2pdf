import os
import platform
from fpdf import FPDF
import argparse
import glob
from PIL import Image
from colorama import init, Fore, Style
import subprocess
import math

parser = argparse.ArgumentParser()
parser.add_argument("path", type=str)
parser.add_argument("dpi", type=int)
parser.add_argument("override", type=int)
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
print(Style.BRIGHT + "Converting " + str(num_images) +
      " images to PDFs at a quality of " + str(args.dpi) + "DPI." + Style.NORMAL)
print("____________________________________________________\n")

max_spaces = math.floor(math.log10(len(images)))

for image in images:
    absolute_path = os.path.dirname(os.path.abspath(image))
    folder_name = os.path.split(absolute_path)[1]
    pdf_filename = os.path.splitext(os.path.basename(image))[0] + ".pdf"
    ps_filename = os.path.splitext(os.path.basename(image))[0] + ".ps"
    absolute_pdf_filename = os.path.sep.join([absolute_path, pdf_filename])
    absolute_ps_filename = os.path.sep.join([absolute_path, ps_filename])

    spaces = max_spaces-math.floor(math.log10(i+1))
    space = ''
    for p in range(0, spaces):
        space = space + ' '

    if os.path.exists(absolute_pdf_filename) and args.override == 0:
        print(Fore.YELLOW + "File (" + space + Fore.MAGENTA + Style.BRIGHT + str(i + 1) + Style.NORMAL
              + Fore.YELLOW + "/" + Fore.MAGENTA + str(num_images) + Fore.YELLOW + "): " + Fore.YELLOW + Style.NORMAL + folder_name + "/" + pdf_filename + " already exists.")
        i = i + 1
        continue

    print("Generating PDF file (" + space + Fore.MAGENTA + Style.BRIGHT + str(i + 1) + Style.NORMAL
          + Fore.CYAN + "/" + Fore.MAGENTA + str(num_images) + Fore.CYAN + "): " + folder_name + "/" + pdf_filename)

    with Image.open(str(image), "r") as img:
        width_px, height_px = img.size
        width_in = width_px/args.dpi
        height_in = height_px/args.dpi

        pdf = FPDF(unit='in', format=tuple((width_in, height_in)))
        pdf.add_page()
        pdf.image(image, 0, 0, width_in, height_in)

        pdf.output(absolute_pdf_filename, "F")

    # We need to convert the PDF to PS and back because of some meta data that is added by FPDF which Latex doesn't like
    if platform.system() == 'Linux':
        subprocess.check_output(
            ['pdf2ps', absolute_pdf_filename, absolute_ps_filename])

        subprocess.check_output(
            ['ps2pdf', absolute_ps_filename, absolute_pdf_filename])

        subprocess.check_output(['rm', absolute_ps_filename])

    i = i + 1


print(Style.RESET_ALL)
