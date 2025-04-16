import json
from difflib import SequenceMatcher

similarity_threshold=0.7

def load_json(file):
    with open(file, "r", encoding="utf-8") as f:
        return json.load(f)

def normalize_title(title):
    return title.lower().replace(" ", "").replace(",", "").replace("-", "").replace(".", "")

def find_exact_matches(ref_a, ref_b, output_file):
    result = []
    for a in ref_a:
        title_a = normalize_title(a["title"])
        match = next((b for b in ref_b if normalize_title(b["title"]) == title_a), None)
        result.append({
            "paper1_ref_num": a["ref_num"],
            "paper1_title": a["title"],
            "paper2_ref_num": match["ref_num"] if match else None
        })
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    print(f"✅ Exact matches saved to {output_file}")

def find_similar_matches(ref_a, ref_b, output_file, threshold=similarity_threshold):
    result = []
    for a in ref_a:
        best_match = None
        best_ratio = 0
        for b in ref_b:
            ratio = SequenceMatcher(None, a["title"], b["title"]).ratio()
            if ratio > best_ratio:
                best_match = b
                best_ratio = ratio
        if best_ratio >= threshold:
            result.append({
                "paper1_ref_num": a["ref_num"],
                "paper1_title": a["title"],
                "paper2_ref_num": best_match["ref_num"],
                "paper2_similar_title": best_match["title"],
                "similarity": round(best_ratio * 100, 2)
            })
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    print(f"✅ Similar matches (≥ {int(threshold*100)}%) saved to {output_file}")

# Load references
ref1 = load_json("reference1.json")
ref2 = load_json("reference2.json")

# Run match functions in both directions
find_exact_matches(ref1, ref2, "12same.json")
find_similar_matches(ref1, ref2, "12similarities.json")

find_exact_matches(ref2, ref1, "21same.json")
find_similar_matches(ref2, ref1, "21similarities.json")
