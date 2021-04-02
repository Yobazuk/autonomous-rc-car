import pygame
from time import sleep


class Joystick:
    def __init__(self, joystick_number=0):

        self.joystick = joystick_number
        self._buttons = {'x': 0, 'o': 0, 't': 0, 's': 0, 'L1': 0, 'R1': 0, 'L2': 0, 'R2': 0, 'share': 0, 'options': 0,
                         'axis1': 0., 'axis2': 0., 'axis3': 0., 'axis4': 0.}
        self._axis = [0., 0., 0., 0., 0., 0.]

        self.__setup__()

    def __setup__(self):
        pygame.init()
        self.joystick = pygame.joystick.Joystick(self.joystick)
        self.joystick.init()

    def assign(self, event, items, value):
        for x, (key, val) in items:
            if x < 10:
                if event.button == x:
                    self._buttons[key] = value

    def get_buttons(self, t=0):

        for event in pygame.event.get():
            if event.type == pygame.JOYAXISMOTION:
                self._axis[event.axis] = round(event.value, 2)
            elif event.type == pygame.JOYBUTTONDOWN:
                self.assign(event, enumerate(self._buttons.items()), 1)
            elif event.type == pygame.JOYBUTTONUP:
                self.assign(event, enumerate(self._buttons.items()), 0)

        self._buttons['axis1'], self._buttons['axis2'], self._buttons['axis3'], self._buttons['axis4'] = \
            [self._axis[0], self._axis[1], self._axis[3], self._axis[4]]

        sleep(t)

        return self._buttons
