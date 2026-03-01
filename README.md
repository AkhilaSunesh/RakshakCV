# RakshakCV 🛡️
> **Empowering road safety through intelligent vigilance.**

RakshakCV is a real-time, AI-powered computer vision pipeline designed to detect motorcycle helmets. Built to enhance road safety compliance, this lightweight system uses deep learning to process live video feeds and instantly classify subjects with highly accurate bounding boxes.

## 🚀 Key Features & Hackathon Highlights
* **Real-Time Edge Inference:** Optimized for live webcam feeds with minimal latency using the Nano architecture.
* **Active Edge-Case Handling (Hard Negative Mining):** Standard models often misclassify regional attire (shawls, dupattas) or winter wear (beanies, hoodies) as helmets due to texture overlap. RakshakCV's dataset was actively fine-tuned with targeted hard-negative images to intelligently differentiate between protective helmets and standard headwear.
* **Flexible CLI:** Easily switch between live webcam evaluation and pre-recorded video testing for robust demonstrations.

## 💻 Tech Stack
* **Language:** Python 3.x
* **Computer Vision & AI:** Ultralytics (YOLOv8), PyTorch, OpenCV
* **Environment:** Model architecture trained utilizing GPU compute, deployed locally for offline edge inference.

## 🛠️ Installation
Ensure you have Python installed, then set up your local environment:

```bash
# Clone the repository
git clone [https://github.com/yourusername/RakshakCV.git](https://github.com/yourusername/RakshakCV.git)
cd RakshakCV

# Install dependencies
pip install ultralytics opencv-python
