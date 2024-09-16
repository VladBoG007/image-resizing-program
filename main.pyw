import os
import customtkinter as ctk
from tkinter import filedialog
from PIL import Image, ImageOps

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

def resize_with_padding(image_path, output_path, size=(1200, 1200), color=(255, 255, 255)):
    image = Image.open(image_path)
    
    image_ratio = image.width / image.height
    target_ratio = size[0] / size[1]
    
    if image_ratio > target_ratio:
        new_width = size[0]
        new_height = int(new_width / image_ratio)
    else:
        new_height = size[1]
        new_width = int(new_height * image_ratio)
    
    resized_image = image.resize((new_width, new_height), Image.ANTIALIAS)
    
    new_image = Image.new("RGB", size, color)
    
    paste_position = ((size[0] - new_width) // 2, (size[1] - new_height) // 2)
    
    new_image.paste(resized_image, paste_position)
    
    new_image.save(output_path)

def process_selected_image(width, height, color, image_path):
    size = (width, height)
    output_dir = "images"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    output_path = os.path.join(output_dir, f"resized_{os.path.basename(image_path)}")
    
    resize_with_padding(image_path, output_path, size=size, color=color)
    print(f"Изображение {image_path} изменено и сохранено как {output_path}")
    result_label.configure(text=f"Изображение сохранено как {output_path}", text_color="green")

def parse_hex_color(hex_color):
    hex_color = hex_color.lstrip('#')
    
    if len(hex_color) == 3:
        hex_color = ''.join([char * 2 for char in hex_color])
    
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def on_save_button_click():
    try:
        width = int(width_entry.get())
        height = int(height_entry.get())
        color = color_entry.get()

        if not color.startswith('#'):
            raise ValueError("Цвет должен начинаться с '#'")
        
        rgb_color = parse_hex_color(color)
        
        if not selected_image_path:
            raise ValueError("Пожалуйста, выберите изображение")

        process_selected_image(width, height, rgb_color, selected_image_path)
    except Exception as e:
        result_label.configure(text=f"Ошибка: {e}", text_color="red")

def on_browse_button_click():
    global selected_image_path
    selected_image_path = filedialog.askopenfilename(
        title="Выбрать изображение", 
        filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif")]
    )
    if selected_image_path:
        selected_image_label.configure(text=f"Выбрано: {os.path.basename(selected_image_path)}")

root = ctk.CTk()
root.title("Изменение размера изображений")
root.geometry("400x350")

width_label = ctk.CTkLabel(root, text="Ширина (px):")
width_label.grid(row=0, column=0, padx=10, pady=10)
width_entry = ctk.CTkEntry(root, width=120, text_color="#00ffcc")
width_entry.grid(row=0, column=1, padx=10, pady=10)
width_entry.insert(0, "600")

height_label = ctk.CTkLabel(root, text="Высота (px):")
height_label.grid(row=1, column=0, padx=10, pady=10)
height_entry = ctk.CTkEntry(root, width=120, text_color="#00ffcc")
height_entry.grid(row=1, column=1, padx=10, pady=10)
height_entry.insert(0, "600")

color_label = ctk.CTkLabel(root, text="Цвет (HEX):")
color_label.grid(row=2, column=0, padx=10, pady=10)
color_entry = ctk.CTkEntry(root, width=120, text_color="#00ffcc")
color_entry.grid(row=2, column=1, padx=10, pady=10)
color_entry.insert(0, "#ffffff")

browse_button = ctk.CTkButton(root, text="Обзор", command=on_browse_button_click)
browse_button.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

selected_image_label = ctk.CTkLabel(root, text="Файл не выбран")
selected_image_label.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

save_button = ctk.CTkButton(root, text="Сохранить", command=on_save_button_click)
save_button.grid(row=5, column=0, columnspan=2, padx=10, pady=20)

result_label = ctk.CTkLabel(root, text="")
result_label.grid(row=6, column=0, columnspan=2, padx=10, pady=10)

selected_image_path = None

root.mainloop()
