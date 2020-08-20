from filters import Cartoonizer
import cv2

video_capture = cv2.VideoCapture(0)
img_counter = 0
while True:
    # Captures video_capture frame by frame
    _, capture = video_capture.read()

    # To capture image in monochrome
    # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # if hasattr(cv2, 'cv'):
    #     capture.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH, 640)
    #     capture.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, 480)
    # else:
    #     capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    #     capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        # calls the detect() function
    # canvas, snap = detect(gray, frame,img_counter)
    # print("*****", type(capture))
    # print(capture)
    # gray = cv2.cvtColor(capture, cv2.COLOR_BGR2GRAY)
    # cv2.imshow('Video1', capture)

    canvas = Cartoonizer().render(capture)
    img_counter += 1
    final = cv2.hconcat([capture, canvas])
    # Displays the result on camera feed
    cv2.imshow('Video', final)

    # if snap:
    #     cv2.waitKey(5000)

    # The control breaks once q key is pressed
    if cv2.waitKey(1) & 0xff == ord('q'):
        break

# Release the capture once all the processing is done.
video_capture.release()
cv2.destroyAllWindows()
