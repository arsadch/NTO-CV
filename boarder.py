import cv2
import numpy as np


class Boarder:
    def __init__(self, callback=None):
        self.callback = callback
        self.borders = None
        self.board = None
        self.x, self.y, self.w, self.h = None, None, None, None
        self.mtx = None
        self.dist = None

    @staticmethod
    def __color_correction(board):
        gamma = 2
        bright = 2
        contrast = 0.8

        hsv = cv2.cvtColor(board, cv2.COLOR_BGR2HSV)

        hsv[:, :, 2] = hsv[:, :, 2] * contrast

        board = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

        rgb = cv2.cvtColor(board, cv2.COLOR_BGR2RGB)

        rgb = np.float32(rgb) / 255.0

        adjusted = np.power(rgb, gamma) * 255.0

        board = cv2.cvtColor(adjusted.astype(np.uint8), cv2.COLOR_RGB2BGR)

        board = cv2.multiply(board, bright)

        board = board.astype(np.float32)

        board *= 0.5

        board = board.astype(np.uint8)

        return board

    def __get_board(self, frame):
        frame = self.__color_correction(frame)

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
        contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        borderss = []
        for contour in contours:
            perimeter = cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, 0.02 * perimeter, True)
            if len(approx) == 4 and perimeter > 500:
                borderss.append(contour)

        if borderss:
            self.borders = sorted(borderss, key=cv2.contourArea)[0]

        if self.borders is not None:
            self.x, self.y, self.w, self.h = cv2.boundingRect(self.borders)

    def run(self):
        cap = cv2.VideoCapture(0)

        while True:
            _, frame = cap.read()

            if not self.x:
                self.__get_board(frame)

            if self.x:
                x, y, w, h = cv2.boundingRect(self.borders)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.imshow('frame', frame)

                self.board = frame[self.y + 10:self.y + self.h - 10, self.x + 10:self.x + self.w - 10]
                self.board = self.__color_correction(self.board)
            if self.callback is not None:
                self.callback(self.board)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()


if __name__ == '__main__':
    pr = Boarder(callback=None)

    pr.run()
