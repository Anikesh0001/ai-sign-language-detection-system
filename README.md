# AI-Powered Sign Language Detection System

A real-time sign language detection and translation system using AI, computer vision, and text-to-speech technology.

## Features

- Real-time hand gesture detection using MediaPipe Hands
- Sign language classification using deep learning
- Text-to-speech feedback for detected signs
- Modern web interface with real-time video feed
- History log of detected signs
- Responsive design for various screen sizes

## Tech Stack

### Backend
- Python
- OpenCV for computer vision
- MediaPipe for hand tracking
- TensorFlow for sign language classification
- FastAPI for the web server
- pyttsx3 for text-to-speech

### Frontend
- Next.js 14
- React
- TypeScript
- Tailwind CSS
- Framer Motion for animations
- WebSocket for real-time communication

## Setup

### Backend Setup

1. Create a Python virtual environment:
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Start the backend server:
   ```bash
   python inference_server.py
   ```

### Frontend Setup

1. Install Node.js dependencies:
   ```bash
   npm install
   ```

2. Start the development server:
   ```bash
   npm run dev
   ```

3. Open [http://localhost:8000](http://localhost:8000) in your browser.

## Usage

1. Position your hands clearly in front of your camera in good lighting.
2. Make clear hand gestures for American Sign Language letters and words.
3. The system will detect your gestures in real-time and:
   - Display the detected sign
   - Provide audio feedback through text-to-speech
   - Add the sign to the history log

## Project Structure

```
.
├── backend/
│   ├── gesture_detection.py    # Hand gesture detection using MediaPipe
│   ├── model_training.py       # Sign language classification model
│   ├── inference_server.py     # FastAPI server for real-time processing
│   ├── tts_integration.py      # Text-to-speech integration
│   └── requirements.txt        # Python dependencies
├── src/
│   ├── app/
│   │   ├── page.tsx           # Main application page
│   │   └── layout.tsx         # Root layout component
│   └── components/
│       ├── VideoFeed.tsx      # Webcam feed component
│       ├── DetectedSign.tsx   # Current sign display
│       └── HistoryLog.tsx     # Sign history component
└── package.json               # Node.js dependencies
```

## Development

### Training Custom Models

To train the model on your own dataset:

1. Prepare your dataset in the required format
2. Modify the training parameters in `model_training.py`
3. Run the training script:
   ```bash
   python model_training.py
   ```

### Adding New Features

1. Backend:
   - Add new Python modules in the `backend/` directory
   - Update `inference_server.py` to handle new functionality
   - Add any new dependencies to `requirements.txt`

2. Frontend:
   - Add new components in `src/components/`
   - Update `page.tsx` to integrate new components
   - Add new styles using Tailwind CSS

## Contributing

1. Fork the repository
2. Create a new branch for your feature
3. Make your changes
4. Submit a pull request

## License

MIT License - feel free to use this project for your own purposes.
