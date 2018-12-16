import math
import pygame
import sys
from pygame.locals import *
from enum import Enum


class Status(Enum):
    STOPPED = (255, 255, 255)
    ACCELERATING = (0, 255, 0)
    CRUISING = (255, 255, 0)
    BRAKING = (255, 0, 0)


class Vehicle:
    def __init__(self, c_id, top_speed, acceleration, follow_distance, lookahead_distance, current_speed):
        self.c_id = c_id
        self.top_speed = top_speed
        self.acceleration = acceleration
        self.follow_distance = follow_distance + 5
        self.lookahead_distance = lookahead_distance

        self.current_speed = current_speed
        self.current_acceleration = acceleration
        self.status = Status.BRAKING
        if self.current_speed > 0:
            self.status = Status.CRUISING


class Lane:
    def __init__(self, length):
        # a lane contains a dictionary of cars, where there forward
        # distance is the key
        self.cars = {}
        # forward length of a lane
        self.length = length

    def get_car_by_id(self, c_id):
        for x in self.cars.keys():
            if self.cars[x].c_id == c_id:
                return self.cars[x]

    def process(self):
        # determine whether cars should speed up
        for current_x in sorted(self.cars.keys(), reverse=True):
            # look ahead within follow distance
            ahead_x = current_x + self.cars[current_x].follow_distance
            should_accelerate = True
            for forward_x in sorted(self.cars.keys()):
                if current_x < forward_x <= ahead_x:
                    # a car within follow distance, don't accelerate
                    should_accelerate = False
                    self.cars[current_x].status = Status.CRUISING
                    break
            if should_accelerate:
                # no cars in follow distance, set current acceleration to acceleration attribute
                self.cars[current_x].current_acceleration = self.cars[current_x].acceleration
                self.cars[current_x].status = Status.ACCELERATING

        # brake if car within lookahead distance
        for current_x in sorted(self.cars.keys(), reverse=True):
            # look ahead within lookahead distance
            ahead_x = current_x + self.cars[current_x].lookahead_distance + self.cars[current_x].follow_distance
            for forward_x in sorted(self.cars.keys()):
                if current_x < forward_x <= ahead_x and self.cars[current_x].current_speed > 0:
                    # a car within lookahead+follow distance, set negative acceleration
                    self.cars[current_x].status = Status.BRAKING
                    numerator = (self.cars[forward_x].current_speed - self.cars[current_x].current_speed)
                    denominator = (forward_x - self.cars[current_x].follow_distance - current_x) / self.cars[current_x].current_speed
                    self.cars[current_x].current_acceleration = \
                        numerator / \
                        (denominator, 1)[denominator == 0]
                    break

        # modify speed based on acceleration
        for current_x in sorted(self.cars.keys(), reverse=True):

            self.cars[current_x].current_speed += self.cars[current_x].current_acceleration

            # set statuses
            if self.cars[current_x].current_speed > self.cars[current_x].top_speed:
                self.cars[current_x].current_speed = self.cars[current_x].top_speed
                self.cars[current_x].status = Status.CRUISING
                self.cars[current_x].current_acceleration = 0
            if self.cars[current_x].current_speed <= 0:
                self.cars[current_x].current_speed = 0
                self.cars[current_x].status = Status.STOPPED
            if self.cars[current_x].current_acceleration < 0 and self.cars[current_x].current_speed == 0:
                self.cars[current_x].current_acceleration = 0
                self.cars[current_x].status = Status.STOPPED

        # move cars along
        for current_x in sorted(self.cars.keys(), reverse=True):
            new_position = current_x + self.cars[current_x].current_speed
            if new_position >= self.length:
                self.cars[new_position-self.length] = self.cars.pop(current_x)
            else:
                self.cars[new_position] = self.cars.pop(current_x)


def print_lane(lane_input):
    for current_x in sorted(lane_input.cars.keys(), reverse=True):
        print(str(lane_input.cars[current_x].c_id) + " - x " + str(current_x) +
              " - speed " + str(lane_input.cars[current_x].current_speed) +
              " - acceleration " + str(lane_input.cars[current_x].current_acceleration))


def print_lane_adv(lane_input):
    top_line = ""
    bottom_line = ""
    cars_line = ""
    for current_x in range(lane_input.length):
        top_line += "-"
    for current_x in range(lane_input.length):
        if current_x in lane_input.cars:
            cars_line += lane_input.cars[current_x].status.value
        else:
            cars_line += " "
    for current_x in range(lane_input.length):
        bottom_line += "-"
    print(top_line)
    print(cars_line)
    print(bottom_line)


def main():
    print("starting...")

    # set up lanes
    lanes = [Lane(800)]

    #lanes[0].cars[500] = Vehicle("carX", 0, 2, 5, 12, 0)

    # set up window
    pygame.init()
    canvas = pygame.display.set_mode((1000, 500))
    pygame.display.set_caption("tffc-sim")
    clock = pygame.time.Clock()

    x = 0

    #for x in range(1, 150):
    while True:
        # handle keys
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit(0)
            if event.type == KEYDOWN and event.key == K_s:
                lanes[0].cars[x] = Vehicle("car" + str(x), 10, 1, 10, 50, 0)
                x += 1

        # wipe display
        canvas.fill((0, 0, 0))

        # process lanes
        lanes[0].process()
        print_lane(lanes[0])

        # draw current lanes
        for lane in lanes:
            pygame.draw.rect(canvas, (255, 255, 255), (100, 200, lane.length, 2))

            # draw cars in current lane
            for current_x in sorted(lane.cars):
                pygame.draw.rect(canvas, lane.cars[current_x].status.value, (current_x + 100, (200 + 2 / 2) - (5 / 2), 10, 5))

        pygame.display.flip()
        clock.tick(10)


if __name__ == '__main__':
    main()
