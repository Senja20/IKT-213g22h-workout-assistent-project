from statemachine import StateMachine, State
from functions.calculate_angle_between_points import (  # type: ignore
    calculate_angle_between_points,
)


class Curl(StateMachine):
    State0 = State("down", initial=True)
    State1 = State("first_quadrant")
    State2 = State("second_quadrant")
    State3 = State("third_quadrant")

    ReturnState1 = State("return_fourth_quadrant")
    ReturnState2 = State("return_third_quadrant")
    ReturnState3 = State("return_second_quadrant")

    switch1 = State0.to(State1)
    switch2 = State1.to(State2)
    switch3 = State2.to(State3)
    start_return_to_init_state = State3.to(ReturnState1)

    switch4 = ReturnState1.to(ReturnState2)
    switch5 = ReturnState2.to(ReturnState3)

    to_initial = ReturnState3.to(State0)

    def curl_logic(self, my_angle, counter, stage):

        # Curl counter logic
        if my_angle > 160 and self.current_state.value == "State0":
            stage = "down"
            self.switch1()
        elif my_angle > 160 and self.current_state.value == "ReturnState3":
            self.to_initial()
            counter += 1

        if 160 > my_angle > 100 and self.current_state.value == "State1":
            self.switch2()
        if 160 > my_angle > 100 and self.current_state.value == "ReturnState2":
            self.switch5()

        if 100 > my_angle > 60 and self.current_state.value == "State2":
            self.switch3()
        elif 100 > my_angle > 60 and self.current_state.value == "ReturnState1":
            self.switch4()

        if my_angle < 40 and stage == "down" and self.current_state.value == "State3":
            stage = "up"

            self.start_return_to_init_state()

        return stage, counter, self.current_state.value


class PushUp:
    def __init__(self):
        self.left_hand = Hand()
        self.right_hand = Hand()

    def update_state(
        self,
        shoulder_left,
        elbow_left,
        wrist_left,
        shoulder_right,
        elbow_right,
        wrist_right,
    ):

        self.right_hand.update_state(shoulder_right, elbow_right, wrist_right)
        self.left_hand.update_state(shoulder_left, elbow_left, wrist_left)


class Hand(StateMachine):
    def update_angle(self, shoulder, elbow, wrist):
        self.wrist = wrist
        self.elbow = elbow
        self.shoulder = shoulder
        self.angle = calculate_angle_between_points(shoulder, elbow, wrist)

    State0 = State("init state", initial=True)  # before key point detection
    State1 = State("straight")  # greater than 160 degrees
    State2 = State("bend")  # about 120 degrees
    State3 = State("into the body")  # less than 60 degrees

    switch1 = State0.to(State1)
    switch2 = State1.to(State2)
    switch3 = State2.to(State3)

    ReturnState1 = State("return_fourth_quadrant")
    ReturnState2 = State("return_third_quadrant")
    ReturnState3 = State("return_second_quadrant")

    start_return_to_init_state = State3.to(ReturnState1)

    switch4 = ReturnState1.to(ReturnState2)
    switch5 = ReturnState2.to(ReturnState3)

    to_initial = ReturnState3.to(State0)

    def update_state(self, shoulder, elbow, wrist):

        self.update_angle(shoulder, elbow, wrist)
        print(self.current_state.value)
        if self.angle > 160 and self.current_state.value == "State0":
            self.switch1()
            print(self.current_state.value)
        elif self.angle > 160 and self.current_state.value == "ReturnState3":
            self.to_initial()
            print(self.current_state.value)

        if 160 > self.angle > 100 and self.current_state.value == "State1":
            self.switch2()
            print(self.current_state.value)
        if 160 > self.angle > 100 and self.current_state.value == "ReturnState2":
            self.switch5()
            print(self.current_state.value)

        if 100 > self.angle > 60 and self.current_state.value == "State2":
            self.switch3()
            print(self.current_state.value)
        elif 100 > self.angle > 60 and self.current_state.value == "ReturnState1":
            self.switch4()
            print(self.current_state.value)

        if self.angle < 40 and self.current_state.value == "State3":
            self.start_return_to_init_state()
            print(self.current_state.value)

        return self.current_state.value
