from subprocess import call
import cv2


def init_camera_parameters():
    call(["uvcdynctrl", "-s", "White Balance Temperature, Auto", "0"])
    call(["uvcdynctrl", "-s", "White Balance Temperature", "4000"])
    call(["uvcdynctrl", "-s", "Exposure, Auto", "0"])
    call(["uvcdynctrl", "-s", "Exposure (Absolute)",  "500"])


def test():
    cap = cv2.VideoCapture(0)
    while cap.isOpened():
        ret, frame = cap.read()
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) and 0xFF is ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    init_camera_parameters()
    test()
