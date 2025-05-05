import cv2
import numpy as np
import mediapipe as mp
from tensorflow.keras.models import load_model
from collections import deque

# 설정
SEQ_LEN = 40
FEATURE_SIZE = 180
CONFIDENCE_THRESHOLD = 0.5
DISPLAY_DURATION_FRAMES = 30  # 약 1초 (30FPS 기준)

CLASS_NAMES = {
    0: "STOP",
    1: "PILL",
    2: "DRINK",
    3: "STRETCH"
}

model = load_model("model/behavior_bilstm_model.h5")
sequence = deque(maxlen=SEQ_LEN)
recent_changes = deque(maxlen=5)
last_pred_class = None
med_complete_timer = 0

mp_hands = mp.solutions.hands
mp_pose = mp.solutions.pose
drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(max_num_hands=2, min_detection_confidence=0.5)
pose = mp_pose.Pose()

def is_valid_coord(x): return 0.0 <= x <= 1.0

def extract_features(result_hands, result_pose, prev_feature=None):
    feature = []

    left_hand, right_hand = None, None
    if result_hands.multi_hand_landmarks:
        for i, hand_landmarks in enumerate(result_hands.multi_hand_landmarks):
            label = result_hands.multi_handedness[i].classification[0].label
            if label == 'Left':
                left_hand = hand_landmarks
            elif label == 'Right':
                right_hand = hand_landmarks

    hands_data = [left_hand, right_hand]
    for hand in hands_data:
        if hand:
            for lm in hand.landmark:
                if not (is_valid_coord(lm.x) and is_valid_coord(lm.y)):
                    return None
                feature.extend([lm.x, lm.y, lm.z])
        else:
            feature.extend([0.0] * 63)

    face_indices = [1, 4, 5, 9]
    if result_pose.pose_landmarks:
        for idx in face_indices:
            lm = result_pose.pose_landmarks.landmark[idx]
            feature.extend([lm.x, lm.y, lm.z])
    else:
        feature.extend([0.0] * (len(face_indices) * 3))

    if result_pose.pose_landmarks:
        p = result_pose.pose_landmarks.landmark
        left_angle = np.degrees(np.arccos(np.clip(np.dot(
            np.array([p[11].x, p[11].y, p[11].z]) - np.array([p[13].x, p[13].y, p[13].z]),
            np.array([p[15].x, p[15].y, p[15].z]) - np.array([p[13].x, p[13].y, p[13].z])
        ) / (np.linalg.norm([p[11].x - p[13].x, p[11].y - p[13].y, p[11].z - p[13].z]) *
              np.linalg.norm([p[15].x - p[13].x, p[15].y - p[13].y, p[15].z - p[13].z]) + 1e-6), -1.0, 1.0)))
        right_angle = left_angle
        feature.extend([left_angle, right_angle])
    else:
        feature.extend([0.0, 0.0])

    if prev_feature and len(prev_feature) == len(feature):
        displacement = np.array(feature) - np.array(prev_feature)
        feature.extend(displacement.tolist())
    else:
        feature.extend([0.0] * len(feature))

    return feature

cap = cv2.VideoCapture(0)
print("\U0001F3A5 Real-time medication prediction started. Press 'q' to quit.")

prev_feature = None
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result_hands = hands.process(rgb)
    result_pose = pose.process(rgb)

    if result_hands.multi_hand_landmarks:
        for hand_landmarks in result_hands.multi_hand_landmarks:
            drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
    if result_pose.pose_landmarks:
        drawing.draw_landmarks(frame, result_pose.pose_landmarks, mp_pose.POSE_CONNECTIONS)

    features = extract_features(result_hands, result_pose, prev_feature)
    if features is None:
        cv2.imshow("Prediction", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        continue

    if len(features) != FEATURE_SIZE:
        features += [0.0] * (FEATURE_SIZE - len(features))

    prev_feature = features
    sequence.append(features)

    if len(sequence) == SEQ_LEN:
        input_data = np.expand_dims(sequence, axis=0)
        pred = model.predict(input_data, verbose=0)[0]
        pred_class = np.argmax(pred)
        pred_prob = pred[pred_class]

        print(f"[예측] class: {CLASS_NAMES[pred_class]}, prob: {pred_prob:.2f}, full: {pred}")

        if pred_prob > CONFIDENCE_THRESHOLD:
            if pred_class != last_pred_class:
                recent_changes.append(pred_class)
                last_pred_class = pred_class
                print(f"[변화 감지] recent_changes = {list(recent_changes)}")

            class_name = CLASS_NAMES[pred_class]
            cv2.putText(frame, f"{class_name} ({pred_prob:.2f})", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
        else:
            cv2.putText(frame, "Uncertain", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)

        # 복약 완료 조건 (순서: PILL -> DRINK)
        if 1 in recent_changes and 2 in recent_changes:
            idx_pill = recent_changes.index(1)
            idx_drink = recent_changes.index(2)
            if idx_pill < idx_drink:
                med_complete_timer = DISPLAY_DURATION_FRAMES
                recent_changes.clear()

    if med_complete_timer > 0:
        cv2.putText(frame, "MEDICATION COMPLETE!", (10, 70),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 0), 3)
        med_complete_timer -= 1

    cv2.imshow("Prediction", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
