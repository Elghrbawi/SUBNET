import os
import numpy as np
from PIL import Image
from flask import Flask, render_template, request, redirect, url_for, send_file
from google.colab import drive, files
from pyngrok import ngrok

class ImageTextAuthenticator:
    def __init__(self, drive_path):
        self.drive_path = drive_path

    def mount_drive(self):
        try:
            drive.mount('/content/drive', force_remount=True)
            return True
        except Exception:
            return False

    def compare_images(self, image1_path, image2_path):
        try:
            img1 = Image.open(image1_path).convert('L')
            img2 = Image.open(image2_path).convert('L')
            img1 = img1.resize((100, 100))
            img2 = img2.resize((100, 100))
            arr1 = np.array(img1)
            arr2 = np.array(img2)
            correlation = np.corrcoef(arr1.flatten(), arr2.flatten())[0,1]
            return correlation
        except Exception:
            return 0

    def verify_login(self, login_image_path):
        reference_paths = {
            'admin': os.path.join(self.drive_path, 'admin_reference.png'),
            'user': os.path.join(self.drive_path, 'user_reference.png')
        }
        max_similarity = 0
        matched_type = None
        for user_type, ref_path in reference_paths.items():
            if os.path.exists(ref_path):
                similarity = self.compare_images(login_image_path, ref_path)
                if similarity > max_similarity:
                    max_similarity = similarity
                    matched_type = user_type
        return matched_type, max_similarity

    def get_reference_image(self, user_type):
        ref_path = os.path.join(self.drive_path, f'{user_type}_reference.png')
        if os.path.exists(ref_path):
            return ref_path
        return None

    def update_reference(self, user_type, file_path):
        try:
            ref_path = os.path.join(self.drive_path, f'{user_type}_reference.png')
            Image.open(file_path).save(ref_path)
            return True
        except Exception:
            return False

drive.mount('/content/drive', force_remount=True)

app = Flask(__name__, template_folder='/content/drive/MyDrive/templates')
authenticator = ImageTextAuthenticator('/content/drive/MyDrive')

@app.route("/reference/<user_type>")
def get_reference(user_type):
    if user_type not in ['admin', 'user']:
        return "Invalid reference type", 400
    ref_path = authenticator.get_reference_image(user_type)
    if ref_path:
        return send_file(ref_path, mimetype='image/png')
    return "No reference image found", 404

@app.route("/", methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        if 'file' not in request.files:
            return render_template("index.html", result="No file part", show_admin=False)
        file = request.files['file']
        if file.filename == '':
            return render_template("index.html", result="No selected file", show_admin=False)

        file_path = os.path.join('/content', file.filename)
        file.save(file_path)

        if 'update_ref' in request.form:
            ref_type = request.form.get('ref_type')
            if ref_type in ['admin', 'user']:
                authenticator.update_reference(ref_type, file_path)
                result = f"Updated {ref_type} reference image"
                return render_template("index.html", result=result, show_admin=True, 
                                    ref_type=ref_type, timestamp=os.urandom(8).hex())
            else:
                result = "Invalid reference type"
                return render_template("index.html", result=result, show_admin=True)
        else:
            user_type, similarity = authenticator.verify_login(file_path)
            similarity_percentage = similarity * 100
            if similarity > 0.8:
                result = f"Access granted: {user_type} ({similarity_percentage:.1f}%)"
                return render_template("index.html", result=result, show_admin=(user_type == 'admin'))
            else:
                result = f"Access denied: Similarity {similarity_percentage:.1f}%"
                return render_template("index.html", result=result, show_admin=False)

    return render_template("index.html", show_admin=False)

if __name__ == "__main__":
    public_url = ngrok.connect(5000)
    print(f"Public URL: {public_url}")
    app.run(port=5000)
