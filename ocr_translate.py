import json
from typing import List, Tuple, TypedDict

import pytesseract
import cv2
import argostranslate.package
import argostranslate.translate

# from PIL import Image


class ArgosDict(TypedDict):
    from_name: str
    to_name: str
    from_code: str
    to_code: str


pytesseract.pytesseract.tesseract_cmd = r"/usr/bin/tesseract"

available_langs = pytesseract.pytesseract.get_languages()
argostranslate.package.update_package_index()


def save_ocr(out_json: str) -> None:
    with open(out_json, encoding="utf8", mode="w+") as f_out:
        json.dump(available_langs, f_out, indent=4)


def save_argos(out_json: str) -> None:
    available_packages = argostranslate.package.get_available_packages()
    package_list: List[ArgosDict] = [ 
        { "from_name": p.from_name, "to_name": p.to_name, "from_code": p.from_code, "to_code": p.to_code } 
        for p in available_packages ]
    with open(out_json, encoding="utf8", mode="w+") as f_out:
        json.dump(package_list, f_out, indent=4)


def argos_packages() -> List[ArgosDict]:
    available_packages = argostranslate.package.get_available_packages()
    package_list: List[ArgosDict] = [ 
        { "from_name": p.from_name, "to_name": p.to_name, "from_code": p.from_code, "to_code": p.to_code } 
        for p in available_packages ]
    return package_list


def translate_text(filename: str, ocr_lang: str, from_code: str, to_code: str) -> Tuple[str, str]:
    available_packages = argostranslate.package.get_available_packages()

    img_cv = cv2.imread(filename)

    # Chinese
    img_rgb = cv2.cvtColor(img_cv, cv2.COLOR_BGR2RGB)
    # img_rgb = Image.frombytes('RGB', img_cv.shape[:2], img_cv, 'raw', 'BGR', 0, 0)
    ocr_text = pytesseract.image_to_string(img_rgb, lang=ocr_lang)
    
    if to_code == "en":
        # To English
        package_to_install = filter( lambda x: x.from_code == from_code and x.to_code == to_code, available_packages )
        argostranslate.package.install_from_path(next(package_to_install).download())

        tr_text = argostranslate.translate.translate(ocr_text, from_code, to_code)
    else:
        # To non-English
        package_to_install = filter(lambda x: x.from_code == from_code and x.to_code == "en", available_packages)
        argostranslate.package.install_from_path(next(package_to_install).download())
        package_to_install = filter(lambda x: x.from_code == "en" and x.to_code == to_code, available_packages)
        argostranslate.package.install_from_path(next(package_to_install).download())

        tr_text = argostranslate.translate.translate(ocr_text, from_code, "en")
        tr_text = argostranslate.translate.translate(tr_text, "en", to_code)

    return ocr_text, tr_text


if __name__ == "__main__":
    # save_ocr("ocr.json")
    # save_argos("argos.json")
    
    oct_text, tr_text = translate_text(r"./text.png", "chi_tra", "zh", "ru")
    print( oct_text )
    print( tr_text)
