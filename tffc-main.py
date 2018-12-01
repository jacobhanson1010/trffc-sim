import pygame


class vehicle:
    def __init__(self, id, top_speed, acceleration, follow_distance, t_follow_distance, current_speed):
        self.id = id
        self.top_speed = top_speed
        self.acceleration = acceleration
        self.follow_distance = follow_distance
        self.t_follow_distance = t_follow_distance

        self.current_speed = current_speed


class lane:
    def __init__(self, length):
        # a lane contains a dictionary of cars, where there forward
        # distance is the key
        self.cars = {}
        # forward length of a lane
        self.length = length


def process_lane(lane_input):
    # determine whether cars should speed up or slow down
    for current_x in reversed(range(lane_input.length)):
        if current_x in lane_input.cars:
            # look ahead within follow distance
            should_accelerate = True
            for forward_x in range(current_x, current_x + lane_input.cars[current_x].follow_distance):
                if forward_x + 1 in lane_input.cars:
                    # a car within follow distance
                    lane_input.cars[current_x].current_speed = 0
                    break
                else:
                    # no cars in follow distance, continue accelerating to top speed
                    lane_input.cars[current_x].current_speed += lane_input.cars[current_x].acceleration
                    if lane_input.cars[current_x].current_speed > lane_input.cars[current_x].top_speed:
                        lane_input.cars[current_x].current_speed = lane_input.cars[current_x].top_speed

    # move cars along
    for current_x in reversed(range(lane_input.length)):
        if current_x in lane_input.cars:
            new_position = current_x + lane_input.cars[current_x].current_speed
            lane_input.cars[new_position] = lane_input.cars.pop(current_x)


def print_lane(lane_input):
    for current_x, car in lane_input.cars.items():
        print(str(car.id) + " - " + str(current_x))


def main():
    print("starting...")
    lane_1 = lane(100)
    for i in range(5):
        # adda a new vehicle to the lane
        lane_1.cars[i] = (vehicle("car" + str(i), 10, 1, 2, 1, 0))

    print("lane_1 at 0")
    print_lane(lane_1)

    for x in range(1,6):
        process_lane(lane_1)
        print("lane_1 at " + str(x))
        print_lane(lane_1)


if __name__ == '__main__':
    main()
