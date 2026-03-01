# RakshakCV 🛡️
> **Empowering road safety through intelligent vigilance.**

Motorcycle-related fatalities remain a major safety concern, and helmet compliance is one of the most effective preventive measures. However, real-time automated enforcement systems must perform reliably across:
- Diverse cultural attire
- Occlusions and partial visibility
- Complex traffic backgrounds

RakshakCV addresses these challenges through optimized inference, structured dataset curation, and edge-case-aware training.
## 🚀 Key Features & Highlights
* **Real-Time Edge Inference:** Optimized for live webcam feeds with minimal latency using the Nano architecture.
* **Active Edge-Case Handling (Hard Negative Mining):** Standard models often misclassify regional attire (shawls, dupattas) or winter wear (beanies, hoodies) as helmets due to texture overlap. RakshakCV's dataset was actively fine-tuned with targeted hard-negative images to intelligently differentiate between protective helmets and standard headwear.
* **Flexible CLI:** Easily switch between live webcam evaluation and pre-recorded video testing for robust demonstrations.

## Modes
  
1️⃣  Live Webcam Detection <br>
2️⃣  Image Detection <br>
3️⃣  Video File Detection <br>
4️⃣  YouTube URL Detection <br>
5️⃣  Exit

## 🧠 Edge Cases Explicitly Handled

The model was tested and optimized against the following real-world non-helmet scenarios:

- Shawl / Dupatta wrapped over head  
- Hijab  
- Burqa  
- Abaya  
- Kandura head coverings  
- Sikh Turban  
- Kippah  
- Beanie / Monkey Cap  
- Hoodies  
- Medical mask combined with head covering  

---

## ❓ Why This Is Important
Many generic models incorrectly classify:
- Rounded cloth folds  
- Dark or structured head coverings  
- Winter caps  
- Religious attire  
as protective helmets.

RakshakCV reduces these errors through:
- Iterative hard-negative mining  
- Dataset balancing  
- Confidence threshold tuning  
- Validation-driven refinement  

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
pip install -r requirements.txt

#Run
python detect.py
