import os
import numpy as np
import cv2
from PIL import Image, ImageDraw, ImageFont
import random
import string

SCRIPT_PATH = os.path.dirname(os.path.realpath(__file__))
TEXTS_PATH = os.path.join(SCRIPT_PATH, 'texts')
ALPHABET = string.ascii_lowercase + string.digits + ".,?!() \n"
os.makedirs(TEXTS_PATH, exist_ok=True)

WHITE = 255
BLACK = 0

font_dims = {}
font_dims["Arial"] = (26, 21)
font_dims["Courier_New"] = (29,11)

missing = {}
missing["Arial"] = {}
missing["Courier_New"] = {}

missing["Arial"]["0"] = (0,6)
missing["Arial"]["1"] = (0,6)
missing["Arial"]["2"] = (0,6)
missing["Arial"]["3"] = (0,6)
missing["Arial"]["4"] = (0,6)
missing["Arial"]["5"] = (0,6)
missing["Arial"]["6"] = (0,6)
missing["Arial"]["7"] = (0,6)
missing["Arial"]["8"] = (0,6)
missing["Arial"]["9"] = (0,6)
missing["Arial"]["."] = (20,6)
missing["Arial"][","] = (20,1)
missing["Arial"]["?"] = (0,6)
missing["Arial"]["!"] = (0,6)
missing["Arial"]["("] = (0,0)
missing["Arial"][")"] = (0,0)
missing["Arial"]["a"] = (6,6)
missing["Arial"]["b"] = (0,6)
missing["Arial"]["c"] = (6,6)
missing["Arial"]["d"] = (0,6)
missing["Arial"]["e"] = (6,6)
missing["Arial"]["f"] = (0,6)
missing["Arial"]["g"] = (6,0)
missing["Arial"]["h"] = (0,6)
missing["Arial"]["i"] = (0,6)
missing["Arial"]["j"] = (0,0)
missing["Arial"]["k"] = (0,6)
missing["Arial"]["l"] = (0,6)
missing["Arial"]["m"] = (6,6)
missing["Arial"]["n"] = (6,6)
missing["Arial"]["o"] = (6,6)
missing["Arial"]["p"] = (6,0)
missing["Arial"]["q"] = (6,0)
missing["Arial"]["r"] = (6,6)
missing["Arial"]["s"] = (6,6)
missing["Arial"]["t"] = (0,6)
missing["Arial"]["u"] = (6,6)
missing["Arial"]["v"] = (6,6)
missing["Arial"]["w"] = (6,6)
missing["Arial"]["x"] = (6,6)
missing["Arial"]["y"] = (6,0)
missing["Arial"]["z"] = (6,6)

missing["Courier_New"]["0"] = (0,6)
missing["Courier_New"]["1"] = (0,6)
missing["Courier_New"]["2"] = (0,6)
missing["Courier_New"]["3"] = (0,6)
missing["Courier_New"]["4"] = (0,6)
missing["Courier_New"]["5"] = (0,6)
missing["Courier_New"]["6"] = (0,6)
missing["Courier_New"]["7"] = (0,6)
missing["Courier_New"]["8"] = (0,6)
missing["Courier_New"]["9"] = (0,6)
missing["Courier_New"]["."] = (16,6)
missing["Courier_New"][","] = (16,1)
missing["Courier_New"]["?"] = (0,6)
missing["Courier_New"]["!"] = (0,6)
missing["Courier_New"]["("] = (0,2)
missing["Courier_New"][")"] = (0,2)
missing["Courier_New"]["a"] = (6,6)
missing["Courier_New"]["b"] = (0,6)
missing["Courier_New"]["c"] = (6,6)
missing["Courier_New"]["d"] = (0,6)
missing["Courier_New"]["e"] = (6,6)
missing["Courier_New"]["f"] = (0,6)
missing["Courier_New"]["g"] = (6,0)
missing["Courier_New"]["h"] = (0,6)
missing["Courier_New"]["i"] = (0,6)
missing["Courier_New"]["j"] = (0,0)
missing["Courier_New"]["k"] = (0,6)
missing["Courier_New"]["l"] = (0,6)
missing["Courier_New"]["m"] = (6,6)
missing["Courier_New"]["n"] = (6,6)
missing["Courier_New"]["o"] = (6,6)
missing["Courier_New"]["p"] = (6,0)
missing["Courier_New"]["q"] = (6,0)
missing["Courier_New"]["r"] = (6,6)
missing["Courier_New"]["s"] = (6,6)
missing["Courier_New"]["t"] = (0,6)
missing["Courier_New"]["u"] = (6,6)
missing["Courier_New"]["v"] = (6,6)
missing["Courier_New"]["w"] = (6,6)
missing["Courier_New"]["x"] = (6,6)
missing["Courier_New"]["y"] = (6,0)
missing["Courier_New"]["z"] = (6,6)


def generate_random_text(N):
    if N == 0 : return ""
    chars = ALPHABET
    
    not_nice = [" ", "\n"]
    
    text = random.choice(chars)
    while text in not_nice :
        text = random.choice(chars)
    
    while len(text) < N :
        sign = random.choice(chars)
        while (sign in not_nice) and ((len(text) == N - 1) or (text[-1] in not_nice and text[-1] != sign)) :
            sign = random.choice(chars)
        text += sign
    
    return text

def blacked(image_array):
    mask = np.any(image_array != [255, 255, 255], axis=-1)
    image_array[mask] = [0, 0, 0]
    return image_array

def add_margins(image, text = None, font = None, upper = 0, lower = 0, right = 0, left = 0, color = WHITE) :
    
    if text is not None and font is not None:
        upper, lower = missing[font][text]
        right, left = 0, 0

    h, w = image.shape[:2]
    new_image = np.full((h + lower + upper, w + right + left, 3), color, dtype=np.uint8)
    
    for x in range(h) :
        for y in range(w) :
            new_image[upper + x,right + y] = image[x,y]
    
    return new_image
    

def cut_image(image, text = None, font = None, margin = 0) :
    image_array = np.array(image)
    non_white_cols = np.any(np.any(image_array != [255, 255, 255], axis=-1), axis=1)
    non_white_rows = np.any(np.any(image_array != [255, 255, 255], axis=-1), axis=0)

    minimal_row = float('inf')
    maximal_row = float('-inf')
    minimal_col = float('inf')
    maximal_col = float('-inf')

    for i in range(len(non_white_rows)) :
        val = non_white_rows[i]
        if val :
            minimal_row = min(minimal_row, i)
            maximal_row = max(maximal_row, i + 1)
    for i in range(len(non_white_cols)) :
        val = non_white_cols[i]
        if val :
            minimal_col = min(minimal_col, i)
            maximal_col = max(maximal_col, i + 1)
    
    x_range = maximal_row - minimal_row
    y_range = maximal_col - minimal_col
    
    new_image_array = np.full((y_range, x_range, 3), 255)
    
    for x in range(x_range) :
        for y in range(y_range) :
            new_image_array[y,x] = image_array[minimal_col + y, minimal_row + x]
    
    return add_margins(new_image_array, text, font, upper = margin, lower = margin, right = margin, left = margin)

def create_text_image(text, font_name='Arial', font_size=32, image_size=(800, 600), margin=20, line_spacing=10, letter_spacing=2, mode=None):
    if text == " ":
        return blacked(np.full((font_dims[font_name][0], font_dims[font_name][1], 3), 255))
        
    font_path = os.path.join(SCRIPT_PATH, "fonts", font_name + ".ttf")

    if not os.path.isfile(font_path):
        raise FileNotFoundError(f"Font file not found: {font_path}")

    image = Image.new('RGB', image_size, (255, 255, 255))
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype(font_path, font_size)
    
    max_text_width = 0
    total_text_height = 0
    text_height = font_dims[font_name][0]
    
    line = ""
    for sign in text + "\n":
        if sign == '\n':
            line_width = sum(draw.textbbox((0, 0), ch, font=font)[2] - draw.textbbox((0, 0), ch, font=font)[0] + letter_spacing for ch in line[:-1])
            max_text_width = max(max_text_width, line_width)
            total_text_height += text_height + line_spacing
            line = ""
        else:
            line += sign

    image_width = max_text_width + 2 * margin
    image_height = total_text_height + 3 * margin

    image = Image.new('RGB', (image_width, image_height), (255, 255, 255))
    draw = ImageDraw.Draw(image)

    y_text = margin
    line = ""
    for sign in text + "\n":
        if sign == '\n':
            x_text = 0
            for ch in line:
                draw.text((x_text, y_text), ch, font=font, fill=(0, 0, 0))
                char_width = draw.textbbox((0, 0), ch, font=font)[2] - draw.textbbox((0, 0), ch, font=font)[0]
                x_text += char_width + letter_spacing
            y_text += text_height + line_spacing
            line = ""
        else:
            line += sign
    
    # new_image = deepcopy(np.array(image))
    
    # new_new_image = [[0 for i in range(new_image.shape[1])] for j in range(new_image.shape[0])]
    
    # for x in range(new_image.shape[1]) :
    #     for y in range(new_image.shape[0]) :
    #         if new_image[y, x][0] != 255 and new_image[y, x][1] != 255 and new_image[y, x][2] != 255 :
    #             new_new_image[y][x] = 1
    
    
    # with open("test.txt", "w") as file :
    #     file.write(str(new_new_image))
    
    if mode == "alphabet":
        return blacked(cut_image(image, text, font_name))
    
    return blacked(cut_image(image, margin=10))
    
    # return blacked(np.array(image))


def rotate_image(image, angle):
    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)
    
    # Oblicz nowy rozmiar obrazu, aby zmieścił się po obrocie
    cos = np.abs(np.cos(angle))
    sin = np.abs(np.sin(angle))
    new_w = int((h * sin) + (w * cos))
    new_h = int((h * cos) + (w * sin))
    
    # Przesunięcie do centrum nowego rozmiaru obrazu
    M = cv2.getRotationMatrix2D(center, angle * 180 / np.pi, 1.0)
    M[0, 2] += (new_w / 2) - center[0]
    M[1, 2] += (new_h / 2) - center[1]
    
    # Użyj interpolacji najbliższego sąsiada
    rotated = cv2.warpAffine(image, M, (new_w, new_h), flags=cv2.INTER_NEAREST, borderMode=cv2.BORDER_REPLICATE)
    return rotated


def save_image_and_text(image, text, font_name, mode):
    CURRENT_PATH = TEXTS_PATH
    filenumber = str(len(os.listdir(CURRENT_PATH)) // 2)
    image_name = f'{filenumber}_image_{font_name}_.png'
    text_name = f'{filenumber}_text_{font_name}_.txt'
    
    if mode == "alphabet" :
        CURRENT_PATH = os.path.join(SCRIPT_PATH, "fonts", "alphabets", f"{font_name}_alphabet")
        if text == "." : text = "A"
        elif text == "," : text = "B"
        elif text == "?" : text = "C"
        elif text == "!" : text = "D"
        elif text == "(" : text = "E"
        elif text == ")" : text = "F"
        elif text == " " : text = "Z"
        image_name = f'{text}.png'
    elif mode == "whole_alphabet" :
        image_name = f"image_{font_name}_.png"
        CURRENT_PATH = os.path.join(SCRIPT_PATH, "alpha")
    os.makedirs(CURRENT_PATH, exist_ok=True)
    filenumber = str(len(os.listdir(TEXTS_PATH)) // 2)
    image_filename = os.path.join(CURRENT_PATH, image_name)
    text_filename = os.path.join(CURRENT_PATH, text_name)
    
    cv2.imwrite(image_filename, image)
    print(f"Image saved as {image_filename}")
    if mode not in ["alphabet", "whole_alphabet"] :
        with open(text_filename, 'w') as text_file:
            text_file.write(text)
        print(f"Text saved as {text_filename}")
        
    

def main(text = None, font = "Arial", rotate = True, mode = None, N = 100) :
    global ALPHABET
        
    if text is None :
        text = generate_random_text(N)
    else :
        text = text.lower()
        old_text = text
        text = ""
        for sign in old_text :
            if sign in ALPHABET :
                text += sign
    
    if text == " " : print("SPACE INCOMING")
    
    print(f"Generated text: {text}")
    text_image = create_text_image(text, font_name = font, mode = mode)
    
    font = font.replace("_","")
    
    if rotate :
        random_angle = random.uniform(-np.pi/8, np.pi/8)
        print(f"Random angle (radians): {random_angle}")
        
        text_image = rotate_image(text_image, random_angle)
    
    save_image_and_text(text_image, text, font, mode)

input_text = 'INDUSTRIAL SOCIETY AND ITS FUTURE\nIntroduction\n\n1. The Industrial Revolution and its consequences have been a disaster for the human\nrace. They have greatly increased the life expectancy of those of us who live in\nadvanced countries, but they have destabilized society, have made life unfulfilling,\nhave subjected human beings to indignities, have led to widespread psychological\nsuffering (in the Third World to physical suffering as well) and have inflicted severe\ndamage on the natural world. The continued development of technology will worsen\nthe situation. It will certainly subject human beings to greater indignities and inflict\ngreater damage on the natural world, it will probably lead to greater social disruption\nand psychological suffering, and it may lead to increased physical suffering even in\n“advanced” countries.'

fonts = ["Courier_New", "Arial"]

def generate_images() :
    global input_text, fonts
    
    
    rot = True
    k = 2

    for i in range(k * len(fonts)) :
        input_font = fonts[i%len(fonts)]
        if i > k // 2 : rot = False
        input_text = 'INDUSTRIAL SOCIETY AND ITS FUTURE\nIntroduction\n\n1. The Industrial Revolution and its consequences have been a disaster for the human\nrace. They have greatly increased the life expectancy of those of us who live in\nadvanced countries, but they have destabilized society, have made life unfulfilling,\nhave subjected human beings to indignities, have led to widespread psychological\nsuffering (in the Third World to physical suffering as well) and have inflicted severe\ndamage on the natural world. The continued development of technology will worsen\nthe situation. It will certainly subject human beings to greater indignities and inflict\ngreater damage on the natural world, it will probably lead to greater social disruption\nand psychological suffering, and it may lead to increased physical suffering even in\n“advanced” countries.'
        main(N = 500, text = input_text, rotate = rot, font = input_font)

def generate_letters() :
    global fonts
    for input_font in fonts :
        for sign in ALPHABET :
            if sign == "\n" : continue
            main(text = sign, rotate = False, font = input_font, mode = "alphabet")

def generate_alphabet_images() :
    global fonts
    for font in fonts :
        main(N = 500, text = ALPHABET, rotate = False, font = font, mode = "whole_alphabet")
    

generate_alphabet_images()
generate_letters()
    
generate_images()