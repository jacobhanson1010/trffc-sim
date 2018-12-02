import pygame
from enum import Enum


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
        if current_speed > 0:
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
        for current_x in reversed(range(self.length)):
            if current_x in self.cars:
                # look ahead within lookahead distance
                for forward_x in range(self.cars[current_x].lookahead_distance):
                    lookahead_x = current_x + 1 + forward_x + self.cars[current_x].follow_distance
                    if lookahead_x in self.cars:
                        # a car within lookahead+follow distance, set negative acceleration
                        self.cars[current_x].acceleration = (self.cars[lookahead_x].current_speed - self.cars[current_x].current_speed) / (forward_x + 1)
                        self.cars[current_x].status = Status.BRAKING
                        break

        # determine whether cars should speed up
        for current_x in reversed(range(self.length)):
            if current_x in self.cars:
                # look ahead within follow distance
                should_accelerate = True
                for forward_x in range(current_x, current_x + self.cars[current_x].follow_distance):
                    if forward_x + 1 in self.cars:
                        # a car within follow distance, don't accelerate
                        self.cars[current_x].current_acceleration = 0
                        self.cars[current_x].status = Status.CRUISING
                        should_accelerate = False
                        break
                if should_accelerate and self.cars[current_x].status != Status.BRAKING:
                    # no cars in follow distance, set current acceleration to acceleration attribute
                    self.cars[current_x].current_acceleration = self.cars[current_x].acceleration
                    self.cars[current_x].status = Status.ACCELERATING

        # modify speed based on acceleration
        for current_x in reversed(range(self.length)):
            if current_x in self.cars:
                self.cars[current_x].current_speed += self.cars[current_x].current_acceleration
                if self.cars[current_x].current_speed > self.cars[current_x].top_speed:
                    self.cars[current_x].current_speed = self.cars[current_x].top_speed
                    self.cars[current_x].status = Status.CRUISING

        # move cars along
        for current_x in reversed(range(self.length)):
            if current_x in self.cars:
                new_position = current_x + self.cars[current_x].current_speed
                self.cars[new_position] = self.cars.pop(current_x)


def print_lane(lane_input):
    for current_x, car in lane_input.cars.items():
        print(str(car.c_id) + " - x " + str(current_x) + " - speed " + str(car.current_speed))


def print_lane_adv(lane_input):
    top_line = ""
    bottom_line = ""
    cars_line = ""
    for x in range(lane_input.length):
        top_line += "-"
    for x in range(lane_input.length):
        if x in lane_input.cars:
            cars_line += lane_input.cars[x].status.value
        else:
            cars_line += " "
    for x in range(lane_input.length):
        bottom_line += "-"
    print(top_line)
    print(cars_line)
    print(bottom_line)


def main():
    print("starting...")
    lane_1 = Lane(100)
    for i in range(0, 10, 2):
        # adda a new vehicle to the lane
        lane_1.cars[i] = (Vehicle("car" + str(i), 5, 1, 2, 2, 0))

    print("lane_1 at 0")
    print_lane(lane_1)

    for x in range(1, 100):
        lane_1.process()
        print("lane_1 at " + str(x))
        print_lane_adv(lane_1)
        input("Press Enter to continue...")


if __name__ == '__main__':
    main()
