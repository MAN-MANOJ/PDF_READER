import fitz  # PyMuPDF
import json
import os
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk


# Function to extract text from PDF
def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text_data = {}

    for page_num in range(len(doc)):
        page = doc[page_num]
        text_data[page_num + 1] = page.get_text("text")

    return text_data


# Function to extract images from PDF
def extract_images_from_pdf(pdf_path, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    doc = fitz.open(pdf_path)
    image_data = {}

    for page_num in range(len(doc)):
        page = doc[page_num]
        images = page.get_images(full=True)

        if images:
            image_data[page_num + 1] = []

        for img_index, img in enumerate(images, start=1):
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            image_ext = base_image["ext"]

            image_filename = os.path.join(output_folder, f"page_{page_num+1}_img_{img_index}.{image_ext}")
            with open(image_filename, "wb") as img_file:
                img_file.write(image_bytes)

            image_data[page_num + 1].append(image_filename)

    return image_data


# Function to search for a topic in extracted text
def search_topic(text_data, keyword):
    results = []
    for page_num, text in text_data.items():
        if keyword.lower() in text.lower():
            results.append(f"Page {page_num}: {text[:200]}...")  # Show only first 200 chars for preview

    return results if results else ["No results found."]


# Function to process PDF and save JSON
def process_pdf():
    pdf_path = filedialog.askopenfilename(title="Select PDF File", filetypes=[("PDF Files", "*.pdf")])
    if not pdf_path:
        return

    output_folder = os.path.join(os.path.dirname(pdf_path), "extracted_results")

    text_data = extract_text_from_pdf(pdf_path)
    image_data = extract_images_from_pdf(pdf_path, output_folder)

    result_data = {}
    for page_num in text_data:
        result_data[page_num] = {
            "text": text_data[page_num],
            "images": image_data.get(page_num, [])
        }

    json_filename = os.path.join(output_folder, "extracted_results.json")
    with open(json_filename, "w", encoding="utf-8") as json_file:
        json.dump(result_data, json_file, indent=4, ensure_ascii=False)

    messagebox.showinfo("Success", f"Data extracted & saved at:\n{json_filename}")


# Function to search topic in extracted text
def search_in_json():
    keyword = search_entry.get()
    json_filename = os.path.join("extracted_results", "extracted_results.json")

    if not os.path.exists(json_filename):
        messagebox.showerror("Error", "JSON file not found! Please extract PDF data first.")
        return

    with open(json_filename, "r", encoding="utf-8") as file:
        data = json.load(file)

    text_data = {int(k): v["text"] for k, v in data.items()}
    results = search_topic(text_data, keyword)

    result_text.delete(1.0, tk.END)
    result_text.insert(tk.END, "\n".join(results))


# GUI Setup
root = tk.Tk()
root.title("PDF Topic Extractor")

frame = tk.Frame(root, padx=20, pady=20)
frame.pack()

title_label = tk.Label(frame, text="PDF Topic Extraction", font=("Arial", 16, "bold"))
title_label.grid(row=0, column=0, columnspan=2, pady=10)

process_btn = tk.Button(frame, text="Select & Process PDF", command=process_pdf, bg="blue", fg="white", padx=10)
process_btn.grid(row=1, column=0, columnspan=2, pady=10)

search_label = tk.Label(frame, text="Search Topic:")
search_label.grid(row=2, column=0, padx=5, pady=5)

search_entry = tk.Entry(frame, width=40)
search_entry.grid(row=2, column=1, padx=5, pady=5)

search_btn = tk.Button(frame, text="Search", command=search_in_json, bg="green", fg="white", padx=10)
search_btn.grid(row=3, column=0, columnspan=2, pady=10)

result_text = tk.Text(frame, width=60, height=10, wrap="word")
result_text.grid(row=4, column=0, columnspan=2, pady=10)

root.mainloop()
