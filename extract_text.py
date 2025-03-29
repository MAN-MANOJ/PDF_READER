import fitz  # PyMuPDF
import os
import re
import json  # For saving results

def extract_text_from_pdf(pdf_path):
    """Extracts text from a PDF and stores it with page numbers."""
    doc = fitz.open(pdf_path)
    text_data = {}

    for page_num in range(len(doc)):
        page = doc[page_num]
        text_data[page_num + 1] = page.get_text("text")

    return text_data

def extract_text_and_images(pdf_path, output_folder, pages):
    """Extracts text and images, linking images to nearby text."""

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    doc = fitz.open(pdf_path)
    results = {}

    for page_num in pages:
        page = doc[page_num - 1]  # Convert to zero-based index
        text = page.get_text("text")
        images = page.get_images(full=True)

        # Split text into lines for better keyword detection
        lines = text.split("\n")
        associated_text = {}

        # Look for keywords like "Figure", "Diagram" near images
        for i, line in enumerate(lines):
            if re.search(r'\b(Figure|Diagram|Image|Fig)\b', line, re.IGNORECASE):
                associated_text[i] = line  

        image_filenames = []
        for img_index, img in enumerate(images, start=1):
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            image_ext = base_image["ext"]

            image_filename = os.path.join(output_folder, f"page_{page_num}_img_{img_index}.{image_ext}")
            with open(image_filename, "wb") as img_file:
                img_file.write(image_bytes)

            image_filenames.append(image_filename)
            print(f"Saved: {image_filename}")

        # Store extracted text, images, and linked text
        results[page_num] = {"text": text, "images": image_filenames, "linked_text": associated_text}

    return results

def search_topic(text_data, keyword):
    """Find pages that contain the search keyword."""
    matched_pages = [page_num for page_num, text in text_data.items() if keyword.lower() in text.lower()]
    return matched_pages

def save_results_to_json(results, output_file):
    """Saves extracted text, images, and linked text into a JSON file."""
    with open(output_file, "w", encoding="utf-8") as json_file:
        json.dump(results, json_file, indent=4, ensure_ascii=False)
    print(f"\n✅ Results saved to: {output_file}")

# ✅ Define paths
pdf_file = "sample.pdf"  # Replace with your PDF file path
output_folder = "extracted_results"  
json_output_file = "extracted_results.json"

# ✅ Extract text from PDF
extracted_text_data = extract_text_from_pdf(pdf_file)

# ✅ Search for a topic
search_query = input("Enter a topic to search for related images and text: ")
matched_pages = search_topic(extracted_text_data, search_query)

# ✅ Extract text and images from matched pages
if matched_pages:
    extracted_results = extract_text_and_images(pdf_file, output_folder, matched_pages)
    save_results_to_json(extracted_results, json_output_file)

    # ✅ Display results
    for page, data in extracted_results.items():
        print(f"\n🔹 Page {page}:")
        print("📖 Extracted Text:")
        print(data["text"])
        print("🖼️ Extracted Images:")
        for img in data["images"]:
            print(img)
        print("🔗 Linked Text Near Images:")
        for _, text in data["linked_text"].items():
            print(f"➡️ {text}")

else:
    print("No related images or text found for this topic.")
