import cv2
import time
import mediapipe as mp

# initialize Holistic model and drawing utils
# Note: This allows full-body landmarks detection
mp_holistic = mp.solutions.holistic
holistic_model = mp_holistic.Holistic()
mp_drawing = mp.solutions.drawing_utils

# Open a webcam
# Connect to your default device's default webcam
capture = cv2.VideoCapture(0)

# initialize current and prev time to calculate the recording fps
prevTime = 0
currTime = 0

# main loop
while capture.isOpened():
    # capture frame by frame
    ret, frame = capture.read()

    # resizing the frame for better view
    frame = cv2.resize(frame, (800, 600))

    # converting bgr to rgb
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # make predictions using holistic model
    image.flags.writeable = False
    results = holistic_model.process(image)
    image.flags.writeable = True

    # converting the rbg image back to BGR
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    # draw the facial landmarks
    mp_drawing.draw_landmarks(
        image,
        results.face_landmarks, 
        mp_holistic.FACEMESH_CONTOURS,
        mp_drawing.DrawingSpec(
            color=(255,0,255),
            thickness=1,
            circle_radius=1
        ),
        mp_drawing.DrawingSpec(
            color=(0,255,255),
            thickness=1,
            circle_radius=1
        )
    )

    # draw the right hand land marks
    mp_drawing.draw_landmarks(
        image,
        results.right_hand_landmarks,
        mp_holistic.HAND_CONNECTIONS
    )

    # draw left hand land marks
    mp_drawing.draw_landmarks(
        image,
        results.left_hand_landmarks,
        mp_holistic.HAND_CONNECTIONS
    )

    # calculate fps
    currTime = time.Time()
    fps = 1 / (currTime-prevTime)
    prevTime=currTime

    # display fps
    cv2.putText(image, str(int(fps)) + " FPS", (10, 70), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)

    # display the landmarks mapped image
    cv2.imshow("Facial and Hand Landmarks", image)

    # use key "q" to break the loop
    if cv2.waitKey("q") & 0xFF == ord('q'):
        break

capture.release()
cv2.destroyAllWindows()