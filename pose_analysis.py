import numpy as np

# Mediapipe landmark index mapping
LANDMARKS = {
    "left_shoulder": 11,
    "right_shoulder": 12,
    "left_elbow": 13,
    "right_elbow": 14,
    "left_wrist": 15,
    "right_wrist": 16,
    "left_hip": 23,
    "right_hip": 24,
    "left_knee": 25,
    "right_knee": 26,
    "left_ankle": 27,
    "right_ankle": 28,
}

def get_point(landmarks, name):
    idx = LANDMARKS[name]
    if idx not in landmarks:
        return None
    return (landmarks[idx][0], landmarks[idx][1])

def angle(a, b, c):
    if None in (a, b, c):
        return None
    a, b, c = np.array(a), np.array(b), np.array(c)
    ba = a - b
    bc = c - b
    if np.linalg.norm(ba) < 1e-6 or np.linalg.norm(bc) < 1e-6:
        return None
    cosang = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
    cosang = np.clip(cosang, -1.0, 1.0)
    return np.degrees(np.arccos(cosang))

def is_shoulder_level(landmarks, tol=20):
    left = get_point(landmarks, "left_shoulder")
    right = get_point(landmarks, "right_shoulder")
    if not left or not right:
        return False
    return abs(left[1] - right[1]) <= tol

def is_upright(landmarks, tol=15):
    l_sh, r_sh = get_point(landmarks, "left_shoulder"), get_point(landmarks, "right_shoulder")
    l_hip, r_hip = get_point(landmarks, "left_hip"), get_point(landmarks, "right_hip")
    if None in (l_sh, r_sh, l_hip, r_hip):
        return False
    mid_sh = ((l_sh[0]+r_sh[0])//2, (l_sh[1]+r_sh[1])//2)
    mid_hip = ((l_hip[0]+r_hip[0])//2, (l_hip[1]+r_hip[1])//2)
    dx = abs(mid_sh[0] - mid_hip[0])
    return dx <= tol

def arms_above_head(landmarks):
    l_wrist, r_wrist = get_point(landmarks, "left_wrist"), get_point(landmarks, "right_wrist")
    l_sh, r_sh = get_point(landmarks, "left_shoulder"), get_point(landmarks, "right_shoulder")
    if None in (l_wrist, r_wrist, l_sh, r_sh):
        return False
    shoulder_y = min(l_sh[1], r_sh[1])
    return l_wrist[1] < shoulder_y and r_wrist[1] < shoulder_y

def one_leg_support(landmarks, tol=40):
    l_ankle, r_ankle = get_point(landmarks, "left_ankle"), get_point(landmarks, "right_ankle")
    if None in (l_ankle, r_ankle):
        return False
    return abs(l_ankle[1] - r_ankle[1]) > tol

# -------------------------- POSE CHECKERS --------------------------

def check_tree_pose(landmarks):
    issues = []
    # Knee angle check
    left_knee_angle = angle(get_point(landmarks, "left_hip"),
                            get_point(landmarks, "left_knee"),
                            get_point(landmarks, "left_ankle"))
    if left_knee_angle and left_knee_angle > 175:
        issues.append("Avoid locking your left knee")
    right_knee_angle = angle(get_point(landmarks, "right_hip"),
                             get_point(landmarks, "right_knee"),
                             get_point(landmarks, "right_ankle"))
    if right_knee_angle and right_knee_angle > 175:
        issues.append("Avoid locking your right knee")
    if not is_shoulder_level(landmarks):
        issues.append("Keep your shoulders level")
    if not is_upright(landmarks):
        issues.append("Keep your spine upright")
    if not arms_above_head(landmarks):
        issues.append("Raise your arms above your head")
    if not one_leg_support(landmarks):
        issues.append("Lift one foot for balance")
    return issues

def check_tadasana(landmarks):
    issues = []
    if not is_upright(landmarks):
        issues.append("Keep your spine upright")
    if not is_shoulder_level(landmarks):
        issues.append("Keep your shoulders level")
    if not arms_above_head(landmarks):
        issues.append("Raise your arms above your head")
    return issues

def check_namaste(landmarks, tol=30):
    issues = []
    if not is_upright(landmarks):
        issues.append("Stand tall with a straight spine")
    l_wrist, r_wrist = get_point(landmarks, "left_wrist"), get_point(landmarks, "right_wrist")
    l_sh, r_sh = get_point(landmarks, "left_shoulder"), get_point(landmarks, "right_shoulder")
    if None not in (l_wrist, r_wrist, l_sh, r_sh):
        mid_chest_y = (l_sh[1] + r_sh[1]) // 2
        if abs(l_wrist[0] - r_wrist[0]) > tol or not (l_wrist[1] >= mid_chest_y and r_wrist[1] >= mid_chest_y):
            issues.append("Bring your palms together at your chest")
    else:
        issues.append("Hands not visible for Namaste check")
    return issues

def check_chair_pose(landmarks):
    issues = []
    # Knee bend (both knees)
    l_knee_angle = angle(get_point(landmarks, "left_hip"),
                         get_point(landmarks, "left_knee"),
                         get_point(landmarks, "left_ankle"))
    r_knee_angle = angle(get_point(landmarks, "right_hip"),
                         get_point(landmarks, "right_knee"),
                         get_point(landmarks, "right_ankle"))
    if l_knee_angle and l_knee_angle > 160:
        issues.append("Bend your left knee more")
    if r_knee_angle and r_knee_angle > 160:
        issues.append("Bend your right knee more")
    if not is_upright(landmarks):
        issues.append("Keep your spine upright")
    if not arms_above_head(landmarks):
        issues.append("Raise your arms above your head")
    return issues

# -------------------------- DISPATCHER --------------------------

def analyze_pose(landmarks, pose_name):
    pose_name = pose_name.lower()
    if pose_name == "tree":
        return check_tree_pose(landmarks)
    elif pose_name == "tadasana":
        return check_tadasana(landmarks)
    elif pose_name == "namaste":
        return check_namaste(landmarks)
    elif pose_name in ("chair", "utkatasana"):
        return check_chair_pose(landmarks)
    else:
        return ["Pose not recognized"]
