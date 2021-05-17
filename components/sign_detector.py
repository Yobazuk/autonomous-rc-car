import cv2
import math


MIN_SIGN_DISTANCE = 20


class SignDetector:
    def __init__(self, cascade_classifier):
        self.classifier = cv2.CascadeClassifier(cascade_classifier)
        self.previous = False

    def detect_signs(self, frame):
        found = False
        signs = self.classifier.detectMultiScale(frame)

        if len(signs) == 1:
            color = (150, 0, 0)
            for (x, y, w, h) in signs:
                if self.distance(w * h) <= MIN_SIGN_DISTANCE:
                    if not self.previous:
                        found = True
                        color = (0, 0, 150)
                    self.previous = True
                else:
                    self.previous = False
                cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
        else:
            self.previous = False

        return frame, found

    @staticmethod
    def distance(area):
        f1 = ((2 * math.pow(10, -8)) * math.pow(area, 2)) - (0.0016 * area) + 51.824
        f2 = ((-8 * math.pow(10, -13)) * math.pow(area, 3)) + \
             ((9 * math.pow(10, -8)) * math.pow(area, 2)) - (0.0034 * area) + 64.113
        return (f1 + f2) / 2

