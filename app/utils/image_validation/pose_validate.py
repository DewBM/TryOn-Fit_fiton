import mediapipe as mp
import cv2

def validate_pose(file_path):
    mp_pose = mp.solutions.pose
    pose = mp_pose.Pose(static_image_mode=True)
    image = cv2.imread(file_path)
    results = pose.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    
    errors = []
    if results.pose_landmarks:
        landmarks = results.pose_landmarks.landmark
        # Check for frontal pose: shoulders and hips alignment
        left_shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER]
        right_shoulder = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER]
        left_hip = landmarks[mp_pose.PoseLandmark.LEFT_HIP]
        right_hip = landmarks[mp_pose.PoseLandmark.RIGHT_HIP]

        # x = int(left_shoulder.x * image.shape[1])
        # y = int(left_shoulder.y * image.shape[0])
        # visibility = left_shoulder.visibility
        # if visibility > 0.5:  # Only draw visible landmarks
        #     cv2.circle(image, (x, y), 5, (0, 255, 0), -1)

        # x = int(right_shoulder.x * image.shape[1])
        # y = int(right_shoulder.y * image.shape[0])
        # visibility = right_shoulder.visibility
        # if visibility > 0.5:  # Only draw visible landmarks
        #     cv2.circle(image, (x, y), 5, (255, 0, 0), -1)

        # # Optionally save the marked image
        # output_path = "./uploads/marked_1.jpg"
        # if output_path:
        #     cv2.imwrite(output_path, image)


        if abs(left_shoulder.x - right_shoulder.x) < 0.1:  # Horizontal misalignment
            errors.append("Please face the camera directly (neutral pose).")

        # Check for arm occlusion: Arms should not cross torso
        if landmarks[mp_pose.PoseLandmark.LEFT_ELBOW].y < landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER].y or \
           landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW].y < landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER].y:
            errors.append("Ensure arms are relaxed and not occluding the torso.")
        
        # Check full visibility: Shoulders, hips, and knees
        if any(l.visibility < 0.5 for l in [left_shoulder, right_shoulder, left_hip, right_hip]):
            errors.append("Ensure your full upper body is visible.")
    else:
        errors.append("Pose landmarks could not be detected. Please upload a clearer image.")
    
    pose.close()
    return errors
