import pygame
import pymunk.pygame_util
from random import randrange
from math import sqrt
from predictor import Predictor
import threading

class Board:
    def __init__(self):
        pygame.init()
        pygame.font.init()
        pymunk.pygame_util.positive_y_is_up = False
        self.predictor = Predictor(callback=self.__line)
        self.width = 1280
        self.height = 720
        size = self.width, self.height
        self.FPS = 60
        self.screen = pygame.display.set_mode(size)
        self.clock = pygame.time.Clock()
        self.draw_options = pymunk.pygame_util.DrawOptions(self.screen)
        self.coord = [[10, 10, 10, 10]]
        self.space = pymunk.Space()
        self.space.gravity = 0, 8000

        self.segment_shape = pymunk.Segment(self.space.static_body, (1, self.height), (self.width, self.height), 26)
        self.space.add(self.segment_shape)
        self.segment_shape.elasticity = 0.4
        self.segment_shape.friction = 1.0

    def create_boundaries(self, space, width, height):
        pass
    
    def create_circle(self, space, radius, mass, pos):
        body = pymunk.Body()
        body.position = pos
        shape = pymunk.Circle(body, radius)
        shape.mass = mass
        shape.color = (255, 0, 0, 100)
        space.add(body, shape)
        return shape

    def __line(self, coord):
       self.coord = coord 
        
    def run(self):
        threading.Thread(target =self.predictor.run).start()
        f = pygame.font.Font(None, 36)
        balls = []
        r = 50
        v = 200
        running = True
        while running:
            self.screen.fill((0, 0, 0))
            text_esc = f.render('Press ESC to quit', 1, (255, 0, 0))
            self.screen.blit(text_esc, (0, 0))
            
            for i in self.coord:
                x1, y1, x2, y2 = i
                pygame.draw.line(self.screen, (255, 255, 255), [x1*2, y1*1.5], [x2*2, y2*1.5], 2)
                if len(balls) > 0:
                    for i in balls:
                        if i.clipline((x1, y1), (x2, y2)):
                            print('hit')
                
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        pos = event.pos
                        balls.append([pos[0], pos[1], -v / sqrt(2), v / sqrt(2)])
            
            for ball in balls:
                pygame.draw.circle(self.screen, (255, 255, 255), [int(ball[0]), int(ball[1])], r)
                ball[0] += ball[2] / 60
                ball[1] += ball[3] / 60
                if ball[0] < r or ball[0] > self.width - r:
                    ball[2] = -ball[2]
                if ball[1] < r or ball[1] > self.height - r:
                    ball[3] = -ball[3]


            pygame.display.flip()
            pygame.display.update()
            self.clock.tick(self.FPS)
        pygame.quit()


if __name__ == '__main__':
    Board().run()
