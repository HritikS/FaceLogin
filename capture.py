from flask_opencv_streamer.streamer import Streamer
import cv2

def shot(name):
    port = 5000
    require_login = False
    streamer = Streamer(port, require_login)
    video_capture = cv2.VideoCapture(0)

    while True:
        _, frame = video_capture.read()
        cv2.imshow("Press 'q' to take snap", frame)
        streamer.update_frame(frame)

        if not streamer.is_streaming:
            streamer.start_streaming()

        key = cv2.waitKey(1)
        if key == ord('q'):
            break

    showPic = cv2.imwrite("/home/hritik/Documents/WS/people/" + name + ".jpg", frame)
    video_capture.release()
    del(video_capture)
    cv2.destroyAllWindows

if __name__ == "__main__":
    shot(input("Enter your name: "))