import pygame
from enum import Enum
import numpy as np

class Status(Enum):
    STOPPED = 'X'
    ACCELERATING = 'A'
    CRUISING = 'C'
    BRAKING = 'B'


class Vehicle:
    def __init__(self, c_id, top_speed, acceleration, follow_distance, lookahead_distance, current_speed):
        self.c_id = c_id
        self.top_speed = top_speed
        self.acceleration = acceleration
        self.follow_distance = follow_distance
        self.lookahead_distance = lookahead_distance

        self.current_speed = current_speed
        self.current_acceleration = acceleration
        self.status = Status.STOPPED
        if self.current_speed > 0:
            self.status = Status.CRUISING


class Lane:
    def __init__(self, length):
        # a lane contains a dictionary of cars, where there forward
        # distance is the key
        self.cars = {}
        # forward length of a lane
        self.length = length

    def process(self):

        # brake if car within lookahead distance
        for current_x in sorted(self.cars.keys(), reverse=True):
            # look ahead within lookahead distance
            ahead_x = current_x + .01 \
                          + self.cars[current_x].lookahead_distance + self.cars[current_x].follow_distance
            for forward_x in sorted(self.cars.keys(), reverse=True):
                if current_x < forward_x <= ahead_x:
                    # a car within lookahead+follow distance, set negative acceleration
                    self.cars[current_x].status = Status.BRAKING
                    self.cars[current_x].current_acceleration = (self.cars[ahead_x].current_speed -
                                                                 self.cars[current_x].current_speed) / forward_x
                    break

        # determine whether cars should speed up
        for current_x in sorted(self.cars.keys(), reverse=True):
            # look ahead within follow distance
            should_accelerate = True
            ahead_x = current_x + .01 + self.cars[current_x].follow_distance
            for forward_x in sorted(self.cars.keys(), reverse=True):
                if current_x < forward_x <= ahead_x and self.cars[current_x].status == Status.BRAKING:
                    # a car within follow distance, stop braking
                    self.cars[current_x].current_acceleration = 0
                    self.cars[current_x].status = Status.CRUISING
                    should_accelerate = False
                    break
            if should_accelerate and self.cars[current_x].status != Status.BRAKING:
                # no cars in follow distance, set current acceleration to acceleration attribute
                self.cars[current_x].current_acceleration = self.cars[current_x].acceleration
                self.cars[current_x].status = Status.ACCELERATING

        # modify speed based on acceleration
        for current_x in sorted(self.cars.keys(), reverse=True):
            self.cars[current_x].current_speed += self.cars[current_x].current_acceleration

            if self.cars[current_x].current_speed > self.cars[current_x].top_speed:
                self.cars[current_x].current_speed = self.cars[current_x].top_speed
                self.cars[current_x].status = Status.CRUISING
            if self.cars[current_x].current_speed <= 0:
                self.cars[current_x].current_speed = 0
                self.cars[current_x].status = Status.STOPPED

        # move cars along
        for current_x in sorted(self.cars.keys(), reverse=True):
            new_position = round(current_x + self.cars[current_x].current_speed, 2)
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
    lane_1 = Lane(100.000)
    #for i in range(0, 10, 2):
        # adda a new vehicle to the lane
        #lane_1.cars[i] = Vehicle("car" + str(i/2), 5, 1, 2, 3, 0)
    lane_1.cars[1] = Vehicle("car" + str(1), 5, 1, 2, 3, 0)

    lane_1.cars[50] = Vehicle("carX", 0, 0, 2, 3, 0)

    print("lane_1 at 0")
    print_lane(lane_1)

    for x in range(1, 15):
        lane_1.process()
        print("lane_1 at " + str(x))
        print_lane(lane_1)
        #print_lane_adv(lane_1)
        #input("Press Enter to continue...")


if __name__ == '__main__':
    main()
