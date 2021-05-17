import cv2


class Camera:
    def __init__(self, cap_num=0):
        self.cap = cv2.VideoCapture(cap_num)

    def get_frame(self, preview=False):
        try:
            ret, frame = self.cap.read()
            # frame = cv2.flip(frame, 1)

            self.show_frame(frame, preview=preview)

            return frame
        except Exception as e:
            print(e)

    @staticmethod
    def show_frame(frame, preview=False):
        if preview:
            cv2.imshow('Camera Feed', frame)
            cv2.waitKey(1)

    @staticmethod
    def exit():
        cv2.destroyAllWindows()
