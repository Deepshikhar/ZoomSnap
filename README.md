
# 🧿 ZoomSnap

**ZoomSnap** is a lightweight desktop application built using Python and OpenCV that allows users to:

- Select a region of interest (ROI) from a live webcam feed,
- Instantly zoom into that region,
- Overlay the zoomed-in view in real-time,
- Capture and save the zoomed view as an image with a simple click.

---

## 🔧 Features

- 📷 **Live Webcam Feed**
- 🔍 **Interactive Zooming** by click-dragging to select a region
- 💾 **One-Click Capture** of the zoomed view
- ⚡ **Real-Time Overlay Preview**
- ➕➖ Adjustable zoom level using `+` and `-` keys
- 🖱️ Mouse-based region selection and capture button

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/zoomsnap.git
cd zoomsnap
```

### 2. Install Dependencies

Make sure Python 3.6+ is installed. Then, install required libraries:

```bash
pip install opencv-python numpy
```

### 3. Run the App

```bash
python app.py
```

---

## 🧠 How to Use

* **Select Region to Zoom:** Click and drag the mouse on the live feed.
* **Adjust Zoom Level:** Use `+` to zoom in, `-` to zoom out (up to 4x).
* **Capture Zoomed View:** Click the red `Capture` button or press `c`.
* **Exit:** Press `Esc`.

---

## 📁 Output

Captured zoomed images are saved as:

```
captured_image.png
```

You can modify this filename inside `app.py` (`self.saved_image_path`).

---

## 🛠️ Built With

* [OpenCV](https://opencv.org/) - Computer vision library
* [NumPy](https://numpy.org/) - Array processing

---

## ✨ Future Ideas

* Save multiple images with timestamped filenames
* Support saving raw selected region (not just zoomed overlay)
* GUI with buttons using `Tkinter` or `PyQt`
* Zoom window as a floating panel instead of overlay

---

## 📜 License

This project is open source and available under the MIT License.

---

> *Zoom in. Snap it. Save it. — ZoomSnap*


