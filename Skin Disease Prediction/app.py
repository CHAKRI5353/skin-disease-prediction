import os
from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
from PIL import Image, UnidentifiedImageError
import torch
from transformers import AutoImageProcessor, AutoModelForImageClassification

# ======= Flask Setup =======
app = Flask(__name__)
app.secret_key = "supersecretkey"  # Needed for flash messages
app.config['UPLOAD_FOLDER'] = "static/uploads"
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# ======= Load Hugging Face Model =======
MODEL_ID = "Jayanth2002/dinov2-base-finetuned-SkinDisease"
# The model and processor load weights from the internet on first run
processor = AutoImageProcessor.from_pretrained(MODEL_ID)
model = AutoModelForImageClassification.from_pretrained(MODEL_ID)

# ======= Allowed file extensions =======
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# ======= Flask Routes =======
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if 'image' not in request.files:
            flash("No file part")
            return redirect(request.url)

        file = request.files['image']

        if file.filename == '':
            flash("No selected file")
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

            # ======= Try opening image safely =======
            try:
                image = Image.open(file_path).convert("RGB")
            except UnidentifiedImageError:
                flash("Invalid image file. Please upload a valid image.")
                os.remove(file_path)
                return redirect(request.url)

            # ======= Preprocess and predict =======
            inputs = processor(images=image, return_tensors="pt")
            with torch.no_grad():
                outputs = model(**inputs)

            logits = outputs.logits
            probs = torch.softmax(logits, dim=1).squeeze().tolist()
            labels = model.config.id2label

            # Create results list: [(label, probability), ...]
            results = [(labels[i], p) for i, p in enumerate(probs)]
            results.sort(key=lambda x: x[1], reverse=True)

            predicted_label, probability = results[0]
            is_diseased = predicted_label.lower() != "normal"
            top_results = results[:6]  # Pass top 6 for the list display

            return render_template(
                "index.html",
                prediction=predicted_label,
                probability=probability,
                results=top_results,
                uploaded_image=url_for('static', filename=f'uploads/{filename}'),
                is_diseased=is_diseased,
                model_id=MODEL_ID
            )
        else:
            flash("File type not allowed. Only png, jpg, jpeg are supported.")
            return redirect(request.url)

    return render_template("index.html")


# ======= Run Flask App =======
if __name__ == "__main__":
    app.run(debug=True)