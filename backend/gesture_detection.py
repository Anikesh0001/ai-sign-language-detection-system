import cv2
import mediapipe as mp

class GestureDetector:
    def __init__(self, max_num_hands=2, detection_confidence=0.7, tracking_confidence=0.7):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            max_num_hands=max_num_hands,
            min_detection_confidence=detection_confidence,
            min_tracking_confidence=tracking_confidence
        )
        self.mp_draw = mp.solutions.drawing_utils

    def detect(self, frame):
        # Convert the BGR image to RGB.
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # Process the frame and detect hands.
        results = self.hands.process(rgb_frame)
        hand_landmarks = []
        if results.multi_hand_landmarks:
            for hand_landmark in results.multi_hand_landmarks:
                hand_landmarks.append(hand_landmark)
        return hand_landmarks

    def draw_landmarks(self, frame, hand_landmarks):
        for landmarks in hand_landmarks:
            self.mp_draw.draw_landmarks(
                frame, landmarks, self.mp_hands.HAND_CONNECTIONS)
        return frame

def main():
    cap = cv2.VideoCapture(0)
    detector = GestureDetector()

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        hand_landmarks = detector.detect(frame)
        frame = detector.draw_landmarks(frame, hand_landmarks)

        cv2.imshow("Hand Gesture Detection", frame)
        if cv2.waitKey(1) & 0xFF == 27:  # ESC key to exit
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
