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

    switch_return_state2 = ReturnState1.to(ReturnState2)
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
            self.switch_return_state2()

        if my_angle < 40 and stage == "down" and self.current_state.value == "State3":
            stage = "up"

            self.start_return_to_init_state()

        return stage, counter, self.current_state.value


class Exercise:
    def __init__(self):
        self.left_hand = Hand()
        self.right_hand = Hand()
        self.push_up = PushUp()

    def _use_both_hands(self,shoulder_left,
        elbow_left,
        wrist_left,
        shoulder_right,
        elbow_right,
        wrist_right):

        self.right_hand.update_state(shoulder_right, elbow_right, wrist_right)
        self.left_hand.update_state(shoulder_left, elbow_left, wrist_left)

        if self.right_hand.current_state.value == "State1" and self.left_hand.current_state.value == "State1" and self.push_up.current_state.value == 'none':
            self.push_up.switchInit()
        elif self.right_hand.current_state.value == "ReturnState1" and self.left_hand.current_state.value == "ReturnState1" and self.push_up.current_state.value == 'up':
            self.push_up.switchDown()
        elif self.right_hand.current_state.value == "State1" and self.left_hand.current_state.value == "State1" and self.push_up.current_state.value == 'down':
            self.push_up.switchUp()
            return 1
        elif self.right_hand.current_state.value == "ReturnState1" and self.left_hand.current_state.value == "ReturnState1" and self.push_up.current_state.value == 'up':
            self.push_up.switchDown()

        print('right state', self.right_hand.current_state.value, ' left state ', self.left_hand.current_state.value)

        return 0


    def _use_right_hand(self,shoulder_right,
        elbow_right,
        wrist_right):

        self.right_hand.update_state(shoulder_right, elbow_right, wrist_right)

        if self.right_hand.current_state.value == "State1" and self.push_up.current_state.value == 'none':
            self.push_up.switchInit()
            self.left_hand.to_state_1()
        elif self.right_hand.current_state.value == "ReturnState1" and self.push_up.current_state.value == 'up':
            self.push_up.switchDown()
            self.left_hand.to_return_state_1()
        elif self.right_hand.current_state.value == "State1" and self.push_up.current_state.value == 'down':
            self.push_up.switchUp()
            self.left_hand.to_state_1()
            return 1

        print('right state', self.right_hand.current_state.value, ' push up state ', self.push_up.current_state.value)
        return 0

    def _use_left_hand(self,shoulder_left,elbow_left,wrist_left):

        self.left_hand.update_state(shoulder_left, elbow_left, wrist_left)

        if self.left_hand.current_state.value == "State1" and self.push_up.current_state.value == 'none':
            self.push_up.switchInit()
            self.right_hand.to_state_1()
        elif self.left_hand.current_state.value == "ReturnState1" and self.push_up.current_state.value == 'up':
            self.push_up.switchDown()
            self.right_hand.to_return_state_1()
        elif self.left_hand.current_state.value == "State1" and self.push_up.current_state.value == 'down':
            self.push_up.switchUp()
            self.right_hand.to_state_1()
            return 1
        return 0


    def update_state(
        self,
        shoulder_left,
        elbow_left,
        wrist_left,
        shoulder_right,
        elbow_right,
        wrist_right,
        visibility,
        count
    ):
        l,r = visibility

        if l and r:
            count = count + self._use_both_hands(shoulder_left,
            elbow_left,
            wrist_left,
            shoulder_right,
            elbow_right,
            wrist_right)
        elif l and not r:
            count = count + self._use_left_hand(shoulder_left,
            elbow_left,
            wrist_left)
        elif not l and r:
            count = count + self._use_right_hand(shoulder_right,
                                elbow_right,
                                wrist_right)

        return self.push_up.current_state.value, count

class PushUp(StateMachine):
    none = State("none", initial=True)
    up = State("up")
    down = State("down")

    switchInit = none.to(up)
    switchUp = down.to(up)
    switchDown = up.to(down)



class Hand(StateMachine):
    def update_angle(self, shoulder, elbow, wrist):
        self.wrist = wrist
        self.elbow = elbow
        self.shoulder = shoulder
        self.angle = calculate_angle_between_points(shoulder, elbow, wrist)

    State0 = State("init state", initial=True)
    State1 = State("straight")
    State2 = State("bend")

    switch1 = State0.to(State1)
    switch2 = State1.to(State2)

    ReturnState1 = State("return_third_quadrant")
    ReturnState3 = State("return_second_quadrant")

    start_return_to_init_state = State2.to(ReturnState1)

    switch5 = ReturnState1.to(ReturnState3)

    to_initial = ReturnState3.to(State0)

    # to state 1
    from_state_2_to_state_1 = State2.to(State1)
    from_return_state_2_to_state1 = ReturnState1.to(State1)
    from_return_state_3_to_state1 = ReturnState3.to(State1)

    # to return state 1
    from_state_0_to_return_state_1 = State0.to(ReturnState1)
    from_state_1_to_return_state_1 = State1.to(ReturnState1)
    from_state_2_to_return_state_1 = State2.to(ReturnState1)
    from_return_state_2_to_return_state1 = ReturnState1.to(ReturnState1)
    from_return_state_3_to_return_state1 = ReturnState3.to(ReturnState1)


    def to_state_1(self):
        if self.current_state.value == "State1":
            pass
        elif self.current_state.value == "State0":
            self.switch1()
        elif self.current_state.value == "State2":
            self.from_state_2_to_state_1()
        elif self.current_state.value == "State3":
            self.from_state_3_to_state_1()
        elif self.current_state.value == "ReturnState1":
            self.from_return_state_2_to_state1()
        elif self.current_state.value == "ReturnState3":
            self.from_return_state_3_to_state1()

    def to_return_state_1(self):
        if self.current_state.value == "State1":
            self.from_state_1_to_return_state_1()
        elif self.current_state.value == "State0":
            self.from_state_0_to_return_state_1()
        elif self.current_state.value == "State2":
            self.from_state_2_to_return_state_1()
        elif self.current_state.value == "State3":
            self.from_state_3_to_return_state_1()
        elif self.current_state.value == "ReturnState1":
            pass
        elif self.current_state.value == "ReturnState3":
            self.from_return_state_3_to_return_state1()

    def update_state(self, shoulder, elbow, wrist):

        self.update_angle(shoulder, elbow, wrist)

        if self.angle > 160 and self.current_state.value == "State0":
            self.switch1()
        elif self.angle > 160 and self.current_state.value == "ReturnState3":
            self.to_initial()

        if 160 > self.angle > 100 and self.current_state.value == "State1":
            self.switch2()
        if 160 > self.angle > 100 and self.current_state.value == "ReturnState1":
            self.switch5()

        if self.angle < 100 and self.current_state.value == "State2":
            self.start_return_to_init_state()

        return self.current_state.value

if __name__ == '__main__':
    print('ha loh')