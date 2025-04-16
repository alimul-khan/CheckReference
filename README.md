# CheckReference

Clone it using:
```sh
git clone https://github.com/alimul-khan/CheckReference.git
```

Open the folder in VS Code.

---

## 📁 Setup Instructions

Navigate to your project directory:
```sh
cd path/to/CheckReference
```

Create a virtual environment:
```sh
python3 -m venv venv
```

Activate the virtual environment:

**On Windows**:
```sh
venv\Scripts\activate
```

**On macOS and Linux**:
```sh
source venv/bin/activate
```

Install the required packages:
```sh
pip install -r requirements.txt
```

---

## 🚀 How to Run

Step 1: Extract references from PDFs
```sh
python 1_pdf2ref.py
```

Step 2: Compare the references
```sh
python 2_ref2Compare.py
```
