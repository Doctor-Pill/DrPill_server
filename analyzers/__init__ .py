from analyzers.face_recognition import face
from analyzers.action_detection import action

def get_active_analyzers():
    return [
        face.analyze_frame,
        action.analyze_frame
    ]
