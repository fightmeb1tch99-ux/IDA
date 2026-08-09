#!/usr/bin/env python3
"""
AI Camera Brain - Intelligent Vision and Learning System
Uses webcam feed, local OpenCV processing, and free/open AI APIs (or OpenAI-compatible endpoints)
to analyze frames, detect objects, learn from observations, and build long-term memory.
"""

import os
import sys
import time
import json
import base64
import argparse
from datetime import datetime
import cv2
import numpy as np
import requests
from dotenv import load_dotenv
from colorama import init, Fore, Style

init(autoreset=True)
load_dotenv()

MEMORY_FILE = "camera_memory.json"
CONFIG_FILE = "config.json"

DEFAULT_CONFIG = {
    "api_url": os.getenv("AI_API_URL", "https://api.openai.com/v1"),
    "api_key": os.getenv("AI_API_KEY", "your_free_or_proxy_api_key_here"),
    "model": os.getenv("AI_MODEL", "gpt-4o-mini"),
    "capture_interval": 5,  # seconds between AI analysis frames
    "camera_index": 0,
    "confidence_threshold": 0.5
}

class CameraMemory:
    """Manages long-term learning and memory of observations."""
    def __init__(self, filepath=MEMORY_FILE):
        self.filepath = filepath
        self.memory = self.load()

    def load(self):
        if os.path.exists(self.filepath):
            try:
                with open(self.filepath, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"{Fore.YELLOW}[Warning] Could not load memory: {e}. Starting fresh.")
        return {"observations": [], "learned_objects": {}, "total_sessions": 0}

    def save(self):
        try:
            with open(self.filepath, 'w', encoding='utf-8') as f:
                json.dump(self.memory, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"{Fore.RED}[Error] Could not save memory: {e}")

    def add_observation(self, analysis_text, objects_list):
        timestamp = datetime.now().isoformat()
        entry = {
            "timestamp": timestamp,
            "analysis": analysis_text,
            "objects": objects_list
        }
        self.memory["observations"].append(entry)
        
        # Keep only last 100 observations
        if len(self.memory["observations"]) > 100:
            self.memory["observations"] = self.memory["observations"][-100:]

        for obj in objects_list:
            obj_name = obj.lower().strip()
            if obj_name in self.memory["learned_objects"]:
                self.memory["learned_objects"][obj_name]["count"] += 1
                self.memory["learned_objects"][obj_name]["last_seen"] = timestamp
            else:
                self.memory["learned_objects"][obj_name] = {
                    "first_seen": timestamp,
                    "last_seen": timestamp,
                    "count": 1
                }
        self.save()


class AICameraBrain:
    def __init__(self, config):
        self.config = config
        self.memory = CameraMemory()
        self.running = False
        
    def encode_frame_to_base64(self, frame):
        success, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 85])
        if not success:
            raise ValueError("Failed to encode frame to JPEG")
        return base64.b64encode(buffer).decode('utf-8')

    def analyze_frame_with_ai(self, frame):
        """Sends frame to AI API for deep visual understanding and memory correlation."""
        base64_image = self.encode_frame_to_base64(frame)
        
        url = f"{self.config['api_url'].rstrip('/')}/chat/completions"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.config['api_key']}"
        }
        
        recent_learned = list(self.memory.memory["learned_objects"].keys())[-15:]
        prompt = (
            "You are the brain of an intelligent AI camera that sees and learns everything. "
            "Analyze this camera frame. Provide a concise, insightful description of what is happening, "
            "what objects/people/animals are visible, and any notable changes or activities. "
            f"Previously learned objects memory (for context): {recent_learned}. "
            "Respond strictly in JSON format with keys: "
            "'description' (string summary of the scene), "
            "'objects' (list of detected object strings)."
        )

        payload = {
            "model": self.config["model"],
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            }
                        }
                    ]
                }
            ],
            "max_tokens": 500,
            "response_format": {"type": "json_object"}
        }

        try:
            response = requests.post(url, headers=headers, json=payload, timeout=20)
            if response.status_code != 200:
                return f"API Error ({response.status_code}): {response.text}", []
            
            res_json = response.json()
            content = res_json['choices'][0]['message']['content']
            data = json.loads(content)
            return data.get("description", "No description"), data.get("objects", [])
        except Exception as e:
            return f"Analysis Exception: {str(e)}", []

    def run(self):
        print(f"{Fore.CYAN}=== AI CAMERA BRAIN INITIALIZING ===")
        print(f"{Fore.GREEN}API URL: {self.config['api_url']}")
        print(f"{Fore.GREEN}Model: {self.config['model']}")
        print(f"{Fore.YELLOW}Opening camera index {self.config['camera_index']}...")

        cap = cv2.VideoCapture(self.config['camera_index'])
        if not cap.isOpened():
            print(f"{Fore.RED}[Error] Could not open webcam (index {self.config['camera_index']}).")
            print(f"{Fore.YELLOW}Tip: You can use a video file path or check camera permissions.")
            return

        self.running = True
        self.memory.memory["total_sessions"] += 1
        self.memory.save()

        last_analysis_time = 0
        current_description = "Initializing AI vision..."
        detected_objects = []

        print(f"{Fore.GREEN}Camera Brain is active! Press 'q' to quit, 's' to force snapshot analysis.")

        try:
            while self.running:
                ret, frame = cap.read()
                if not ret:
                    print(f"{Fore.RED}[Error] Failed to grab frame from camera.")
                    break

                current_time = time.time()
                # Run AI analysis at specified intervals
                if current_time - last_analysis_time >= self.config['capture_interval']:
                    last_analysis_time = current_time
                    print(f"{Fore.BLUE}[AI Brain] Analyzing frame...")
                    desc, objs = self.analyze_frame_with_ai(frame)
                    current_description = desc
                    detected_objects = objs
                    self.memory.add_observation(desc, objs)
                    print(f"{Fore.GREEN}[Observation] {desc}")
                    print(f"{Fore.MAGENTA}[Detected Objects] {objs}\n")

                # Overlay info on video frame
                display_frame = frame.copy()
                h, w, _ = display_frame.shape
                
                # Draw translucent status bar
                overlay = display_frame.copy()
                cv2.rectangle(overlay, (0, h - 80), (w, h), (0, 0, 0), -1)
                alpha = 0.6
                cv2.addWeighted(overlay, alpha, display_frame, 1 - alpha, 0, display_frame)

                # Put description text
                short_desc = current_description if len(current_description) < 80 else current_description[:77] + "..."
                cv2.putText(display_frame, f"AI Vision: {short_desc}", (10, h - 50),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
                
                objs_str = ", ".join(detected_objects[:6]) if detected_objects else "Scanning..."
                cv2.putText(display_frame, f"Memory Objects: {objs_str}", (10, h - 20),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

                cv2.imshow("AI Camera Brain", display_frame)

                key = cv2.waitKey(1) & 0xFF
                if key == ord('q'):
                    break
                elif key == ord('s'):
                    print(f"{Fore.YELLOW}[Manual Trigger] Forcing immediate AI analysis...")
                    desc, objs = self.analyze_frame_with_ai(frame)
                    current_description = desc
                    detected_objects = objs
                    self.memory.add_observation(desc, objs)
                    print(f"{Fore.GREEN}[Manual Observation] {desc}\n")

        finally:
            cap.release()
            cv2.destroyAllWindows()
            print(f"{Fore.CYAN}=== AI CAMERA BRAIN SHUT DOWN ===")


def load_config():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                user_cfg = json.load(f)
                cfg = DEFAULT_CONFIG.copy()
                cfg.update(user_cfg)
                return cfg
        except Exception:
            pass
    return DEFAULT_CONFIG


def main():
    parser = argparse.ArgumentParser(description="AI Camera Brain - Intelligent Vision and Learning System")
    parser.add_argument("--camera", type=int, default=None, help="Camera device index")
    parser.add_argument("--interval", type=int, default=None, help="Seconds between AI analysis")
    parser.add_argument("--model", type=str, default=None, help="AI model name")
    parser.add_argument("--setup", action="store_true", help="Interactive setup to configure API key")
    args = parser.parse_args()

    config = load_config()

    if args.setup:
        print(f"{Fore.CYAN}=== AI Camera Brain Interactive Setup ===")
        api_url = input(f"Enter AI API URL [{config['api_url']}]: ").strip()
        if api_url:
            config['api_url'] = api_url
        api_key = input(f"Enter AI API Key [{config['api_key'][:6]}...]: ").strip()
        if api_key:
            config['api_key'] = api_key
        model = input(f"Enter Model Name [{config['model']}]: ").strip()
        if model:
            config['model'] = model
            
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2)
        print(f"{Fore.GREEN}Configuration saved to {CONFIG_FILE}!")
        return

    if args.camera is not None:
        config['camera_index'] = args.camera
    if args.interval is not None:
        config['capture_interval'] = args.interval
    if args.model is not None:
        config['model'] = args.model

    brain = AICameraBrain(config)
    brain.run()


if __name__ == "__main__":
    main()
