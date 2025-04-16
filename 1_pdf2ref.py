import re
import json
import fitz  # PyMuPDF
import os

def pdf_to_text(pdf_file, txt_file):
    doc = fitz.open(pdf_file)
    text = ""
    for page in doc:
        text += page.get_text()
    with open(txt_file, "w", encoding="utf-8") as f:
        f.write(text)
    print(f"📄 Converted {pdf_file} → {txt_file}")

def extract_references(input_file, output_file):
    with open(input_file, "r", encoding="utf-8") as f:
        text = f.read()

    text = text.replace("-\n", "").replace("\n", " ")

    match = re.search(r"REFERENCES\s*(\[1\].+)", text, re.IGNORECASE)
    if not match:
        raise ValueError(f"REFERENCES section not found in {input_file}")

    ref_text = match.group(1)

    ref_pattern = re.compile(r"\[(\d+)\](.+?)(?=\[\d+\]|$)")
    matches = ref_pattern.findall(ref_text)

    references = []
    for ref_num, content in matches:
        full_ref = f"[{ref_num}]{content.strip()}"
        title_match = re.search(r'“([^”]+)”', content)
        title = title_match.group(1).strip() if title_match else ""
        
        references.append({
            "ref_num": int(ref_num),
            "title": title,
            "full_reference": full_ref
        })

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(references, f, indent=2, ensure_ascii=False)

    print(f"✅ Extracted {len(references)} references to {output_file}")

def process_paper(base_name):
    pdf_file = f"{base_name}.pdf"
    txt_file = f"{base_name}.txt"
    json_file = f"reference{base_name[-1]}.json"

    if not os.path.exists(txt_file):
        pdf_to_text(pdf_file, txt_file)
    
    extract_references(txt_file, json_file)

# Process both paper1 and paper2
process_paper("paper1")
process_paper("paper2")
