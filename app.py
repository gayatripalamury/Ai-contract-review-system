from flask import Flask, render_template, request
import os
import fitz  # PyMuPDF

app = Flask(__name__)

# Folder to save uploaded files
UPLOAD_FOLDER = "uploads"
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Analyze the contract based on rules
def analyze_contract(text):
    results = []

    if "termination" not in text.lower():
        results.append("⚠️ 'Termination' clause is missing.")

    if "confidential" not in text.lower():
        results.append("🔒 'Confidentiality' clause is missing.")

    if "jurisdiction" not in text.lower():
        results.append("📍 'Jurisdiction' clause missing (important for legal disputes)")

    if "intellectual property" not in text.lower():
        results.append("🧠 No mention of 'Intellectual Property' ownership")

    if "indemnify" in text.lower() and "indemnification" not in text.lower():
        results.append("⚠️ 'Indemnify' used but no clear indemnification clause")

    if "arbitration" not in text.lower() and "dispute" in text.lower():
        results.append("⚖️ 'Dispute Resolution' present but no 'Arbitration' method mentioned")

    return results

# Home route to upload and review contracts
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files["contract"]
        if file:
            filename = file.filename
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            file.save(filepath)

            # Extract text from uploaded PDF
            doc = fitz.open(filepath)
            full_text = ""
            for page in doc:
                full_text += page.get_text()

            # Analyze the extracted text
            results = analyze_contract(full_text)

            return render_template("result.html", results=results, filename=filename)
    
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)


