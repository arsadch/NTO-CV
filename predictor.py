import cv2
import numpy as np

from boarder import Boarder


class Predictor:
    def __init__(self, callback=None):
        self.boarder = Boarder(callback=self.__process_contours)
        self.callback = callback

    @staticmethod
    def __get_contours(board):
        gray = cv2.cvtColor(board, cv2.COLOR_BGR2GRAY)

        ret, binary = cv2.threshold(gray, 50, 255, cv2.THRESH_BINARY)

        kernel = np.ones((5, 5), np.uint8)
        morphology = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)

        contours, _ = cv2.findContours(morphology, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        cv2.drawContours(board, contours, -1, (0, 255, 0), 2)
        return contours

    def __process_contours(self, board):
        contours = self.__get_contours(board)

        board = cv2.drawContours(board, contours, -1, (0, 255, 0), 2)

        cv2.imshow('board', board)

        if self.callback is not None:
            self.callback(contours)

    def run(self):
        self.boarder.run()


if __name__ == '__main__':
    Predictor().run()
