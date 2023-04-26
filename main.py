import pytesseract
import cv2
import argostranslate.package
import argostranslate.translate
from pprint import pprint


pytesseract.pytesseract.tesseract_cmd = r'./tesseract/tesseract'
img_cv = cv2.imread(r'./text.png')


available_langs = pytesseract.pytesseract.get_languages()
argostranslate.package.update_package_index()
available_packages = argostranslate.package.get_available_packages()
# pprint(available_langs)
# pprint(available_packages)


# By default OpenCV stores images in BGR format and since pytesseract assumes RGB format,
# we need to convert from BGR to RGB format/mode:
img_rgb = cv2.cvtColor(img_cv, cv2.COLOR_BGR2RGB)
ocr_lines = [ _ for _ in pytesseract.image_to_string(img_rgb, lang='chi_sim').split('\n') if _ ]

from_code, to_code = "zh", "ru"

tr_lines = []
if to_code == "en":
    # English text
    package_to_install = filter( lambda x: x.from_code == from_code and x.to_code == to_code, available_packages )
    argostranslate.package.install_from_path(next(package_to_install).download())

    for line in ocr_lines:
        tr_line = argostranslate.translate.translate(line, from_code, to_code)
        item = line, tr_line
        tr_lines.append(item)
else:
    # Non-english text
    package_to_install = filter(lambda x: x.from_code == from_code and x.to_code == "en", available_packages)
    argostranslate.package.install_from_path(next(package_to_install).download())
    package_to_install = filter(lambda x: x.from_code == "en" and x.to_code == to_code, available_packages)
    argostranslate.package.install_from_path(next(package_to_install).download())

    for line in ocr_lines:
        # to eng
        tr_line = argostranslate.translate.translate(line, from_code, "en")
        # to to_code
        tr_line = argostranslate.translate.translate(tr_line, "en", to_code)
        item = line, tr_line
        tr_lines.append(item)

pprint(tr_lines)
