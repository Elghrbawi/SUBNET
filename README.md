![Authentication Flow](Screenshots/cover.PNG)

**ImageTextAuthenticator** is a secure, image-based authentication system. It verifies users by comparing uploaded images with stored references, supporting roles like `admin` and `user` for tailored access control.

### Features
- **Image-based Authentication:** Users upload an image to log in. Similarity with reference images is calculated, granting access based on a threshold.
- **Role Management:** Supports `admin` and `user` roles for customized access.
- **Dynamic Updates:** Admins can update reference images dynamically.
- **Clear Feedback:** Displays authentication status with similarity percentage for transparency.

![Authentication Flow](Screenshots/Auth.PNG)

---

### Installation
1. **Set up Colab Environment:**
    - Mount Google Drive.
    - Upload the required files (`subnet.py`, `index.html`, `ngrok.license`, and `installation.txt`) to a Colab directory.

2. **Install Dependencies:**
    ```bash
    !pip install pytesseract Pillow flask pyngrok
    !apt-get update && apt-get install -y tesseract-ocr
    ```

3. **Configure ngrok:**
    ```bash
    ngrok config add-authtoken $YOUR_AUTHTOKEN
    ```
    Replace `$YOUR_AUTHTOKEN` with the token from `ngrok.license`.

4. **Run the Application:**
    ```bash
    python subnet.py
    ```

### Usage
1. Open the generated public URL provided by ngrok.
2. Upload an image to log in as `admin` or `user`.
3. Admins can update reference images for roles directly via the web interface.

### Live Demo
[Access the live application](https://239f-34-106-146-39.ngrok-free.app/)

![Admin Panel](Screenshots/Admin.PNG)

### Authentication Feedback
Displays user role and similarity percentage:
![Feedback](Screenshots/Access.PNG)

---
For detailed setup, refer to the comments in `subnet.py` or explore the `installation.txt` for step-by-step guidance.

