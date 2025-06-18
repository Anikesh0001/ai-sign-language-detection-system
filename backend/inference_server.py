import asyncio
import base64
import cv2
import numpy as np
from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import json
from typing import List

from gesture_detection import GestureDetector
from model_training import SignLanguageModel
from tts_integration import TextToSpeech

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Modify in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize components
gesture_detector = GestureDetector()
model = SignLanguageModel.load_model('models/sign_language_model.h5')  # Updated path relative to backend directory
tts = TextToSpeech()

class Frame(BaseModel):
    data: str  # Base64 encoded image

def process_frame(frame_data: str):
    """Process a single frame: detect hands and classify gestures"""
    # Decode base64 image
    img_bytes = base64.b64decode(frame_data)
    img_arr = np.frombuffer(img_bytes, dtype=np.uint8)
    frame = cv2.imdecode(img_arr, cv2.IMREAD_COLOR)
    
    # Detect hand landmarks
    hand_landmarks = gesture_detector.detect(frame)
    
    if not hand_landmarks:
        return None, frame
    
    # Process landmarks for classification
    # Note: You'll need to implement preprocessing based on your model's requirements
    processed_hand = preprocess_landmarks(hand_landmarks[0], frame.shape)
    
    # Classify gesture
    prediction = model.predict(processed_hand)
    
    # Draw landmarks on frame
    frame = gesture_detector.draw_landmarks(frame, hand_landmarks)
    
    return prediction, frame

def preprocess_landmarks(landmarks, frame_shape):
    """Convert landmarks to model input format"""
    # Implementation depends on your model's input requirements
    # This is a placeholder - modify based on your needs
    img_size = (64, 64)
    hand_img = extract_hand_region(landmarks, frame_shape, img_size)
    return hand_img

def extract_hand_region(landmarks, frame_shape, target_size):
    """Extract and resize hand region from frame"""
    # Placeholder implementation - modify based on your needs
    # Returns a preprocessed image of the hand region
    return np.zeros((*target_size, 3))  # Placeholder

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    
    try:
        while True:
            # Receive frame from client
            data = await websocket.receive_text()
            frame_data = json.loads(data)
            
            # Process frame
            prediction, processed_frame = process_frame(frame_data['data'])
            
            if prediction is not None:
                # Convert processed frame to base64
                _, buffer = cv2.imencode('.jpg', processed_frame)
                processed_frame_b64 = base64.b64encode(buffer).decode('utf-8')
                
                # Get text for detected sign
                sign_text = get_sign_text(prediction)  # Implement based on your classes
                
                # Generate speech for the detected sign
                audio_data = await tts.generate_speech(sign_text)
                
                # Send results back to client
                response = {
                    'prediction': int(prediction),
                    'sign_text': sign_text,
                    'processed_frame': processed_frame_b64,
                    'audio': base64.b64encode(audio_data).decode('utf-8') if audio_data else None
                }
                
                await websocket.send_json(response)
            else:
                await websocket.send_json({
                    'prediction': None,
                    'message': 'No hands detected'
                })
                
    except Exception as e:
        print(f"WebSocket error: {e}")
    finally:
        await websocket.close()

def get_sign_text(prediction: int) -> str:
    """Convert model prediction to text"""
    # Implement based on your class labels
    # This is a placeholder - modify based on your classes
    signs = ['A', 'B', 'C', 'D', 'E', 'F']  # Add all your classes
    return signs[prediction] if prediction < len(signs) else 'Unknown'

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
