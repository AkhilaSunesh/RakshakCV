import cv2
import sys
import time
import os
import subprocess
import numpy as np
from ultralytics import YOLO

# -----------------------------
# Configuration
# -----------------------------
CONF_THRESHOLD = 0.25  # YOLO confidence threshold

# -----------------------------
# Load YOLO Model
# -----------------------------
print("🛡️  Loading YOLO model...")
yolo_model = YOLO("best.pt")
print("✅ YOLO model loaded.")

# -----------------------------
# Helper Functions
# -----------------------------

def parse_yolo_results(results):
    """Parse YOLO results into a structured list of detections."""
    detections = []
    if results and len(results) > 0:
        result = results[0]
        boxes = result.boxes
        if boxes is not None:
            for i in range(len(boxes)):
                box = boxes.xyxy[i].cpu().numpy()
                conf = float(boxes.conf[i].cpu().numpy())
                cls_id = int(boxes.cls[i].cpu().numpy())
                cls_name = result.names[cls_id] if cls_id in result.names else str(cls_id)
                detections.append({
                    "box": box,
                    "conf": conf,
                    "cls_id": cls_id,
                    "cls_name": cls_name,
                })
    return detections


def annotate_frame(frame, detections):
    """Draw annotated bounding boxes on the frame using YOLO results."""
    annotated = frame.copy()
    color = (0, 255, 0)  # Standard green for all boxes

    for det in detections:
        box = det["box"]
        conf = det["conf"]
        cls_name = det["cls_name"]
        x1, y1, x2, y2 = map(int, box)

        label = f"{cls_name} {conf:.0%}"

        # Draw bounding box
        cv2.rectangle(annotated, (x1, y1), (x2, y2), color, 2)

        # Draw label background
        (label_w, label_h), baseline = cv2.getTextSize(
            label, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2
        )
        cv2.rectangle(
            annotated,
            (x1, y1 - label_h - baseline - 5),
            (x1 + label_w, y1),
            color,
            -1,
        )
        cv2.putText(
            annotated,
            label,
            (x1, y1 - baseline - 2),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (255, 255, 255),
            2,
        )

    return annotated


def add_status_bar(frame, fps=None):
    """Add a status bar at the top of the frame."""
    h, w = frame.shape[:2]
    bar_h = 30
    bar = np.zeros((bar_h, w, 3), dtype=np.uint8)
    bar[:] = (40, 40, 40)

    status = "RakshakCV | Mode: YOLO Only"
    if fps is not None:
        status += f" | FPS: {fps:.1f}"

    cv2.putText(bar, status, (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 1)

    return np.vstack([bar, frame])


# =============================================================
# Detection Modes
# =============================================================

def run_webcam():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("❌ Error: Could not open webcam.")
        return

    print("🎥 Press 'q' to exit webcam mode.")
    prev_time = time.time()

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # YOLO detection
        results = yolo_model(frame, conf=CONF_THRESHOLD, verbose=False)
        detections = parse_yolo_results(results)

        # Annotate
        annotated = annotate_frame(frame, detections)

        # FPS calculation
        curr_time = time.time()
        fps = 1.0 / max(curr_time - prev_time, 0.001)
        prev_time = curr_time

        annotated = add_status_bar(annotated, fps)
        cv2.imshow("RakshakCV - Live Detection", annotated)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()


def run_image():
    path = input("📂 Enter image path: ").strip().strip('"')

    frame = cv2.imread(path)
    if frame is None:
        print("❌ Error: Could not read image.")
        return

    print("🔍 Running YOLO detection...")
    results = yolo_model(frame, conf=CONF_THRESHOLD, verbose=False)
    detections = parse_yolo_results(results)
    print(f"   Found {len(detections)} detection(s).")

    annotated = annotate_frame(frame, detections)
    annotated = add_status_bar(annotated)

    cv2.imshow("RakshakCV - Image Detection", annotated)
    print("Press any key to close the image window.")
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def run_video():
    path = input("🎬 Enter video path: ").strip().strip('"')

    cap = cv2.VideoCapture(path)
    if not cap.isOpened():
        print("❌ Error: Could not open video.")
        return

    print("🎥 Press 'q' to exit video mode.")
    prev_time = time.time()

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # YOLO detection
        results = yolo_model(frame, conf=CONF_THRESHOLD, verbose=False)
        detections = parse_yolo_results(results)

        # Annotate
        annotated = annotate_frame(frame, detections)

        # FPS calculation
        curr_time = time.time()
        fps = 1.0 / max(curr_time - prev_time, 0.001)
        prev_time = curr_time

        annotated = add_status_bar(annotated, fps)
        cv2.imshow("RakshakCV - Video Detection", annotated)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()


def get_youtube_stream_url(youtube_url):
    """Use yt-dlp to extract the best direct stream URL from a YouTube link."""
    try:
        result = subprocess.run(
            ["yt-dlp", "-f", "best[ext=mp4][height<=720]", "--get-url", youtube_url],
            capture_output=True, text=True, timeout=30,
        )
        if result.returncode != 0:
            print(f"   ❌ yt-dlp error: {result.stderr.strip()}")
            return None
        return result.stdout.strip()
    except FileNotFoundError:
        print("❌ yt-dlp not found. Install it with: pip install yt-dlp")
        return None
    except subprocess.TimeoutExpired:
        print("❌ Timed out fetching YouTube stream URL.")
        return None


def run_youtube():
    url = input("🔗 Enter YouTube URL: ").strip().strip('"')

    print("📡 Fetching stream URL from YouTube...")
    stream_url = get_youtube_stream_url(url)
    if stream_url is None:
        return

    cap = cv2.VideoCapture(stream_url)
    if not cap.isOpened():
        print("❌ Error: Could not open YouTube stream.")
        return

    print("🎥 Streaming from YouTube — press 'q' to exit.")
    prev_time = time.time()

    while True:
        ret, frame = cap.read()
        if not ret:
            print("📭 Stream ended.")
            break

        # YOLO detection
        results = yolo_model(frame, conf=CONF_THRESHOLD, verbose=False)
        detections = parse_yolo_results(results)

        # Annotate
        annotated = annotate_frame(frame, detections)

        # FPS calculation
        curr_time = time.time()
        fps = 1.0 / max(curr_time - prev_time, 0.001)
        prev_time = curr_time

        annotated = add_status_bar(annotated, fps)
        cv2.imshow("RakshakCV - YouTube Detection", annotated)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()


# =============================================================
# MENU LOOP
# =============================================================
if __name__ == "__main__":
    while True:
        print("\n🛡️ ===== RakshakCV Helmet Detection =====")
        print("   Mode: YOLO Only")
        print("1️⃣  Live Webcam Detection")
        print("2️⃣  Image Detection")
        print("3️⃣  Video File Detection")
        print("4️⃣  YouTube URL Detection")
        print("5️⃣  Exit")

        choice = input("👉 Enter your choice (1-5): ")

        if choice == "1":
            run_webcam()
        elif choice == "2":
            run_image()
        elif choice == "3":
            run_video()
        elif choice == "4":
            run_youtube()
        elif choice == "5":
            print("👋 Exiting RakshakCV...")
            break
        else:
            print("⚠️ Invalid choice. Please select 1-5.")