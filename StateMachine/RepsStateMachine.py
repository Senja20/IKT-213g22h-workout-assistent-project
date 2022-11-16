from functions.calculate_angle_between_points import (  # type: ignore
    calculate_angle_between_points,
)
from statemachine import State, StateMachine  # type: ignore


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
        self.back = Back()
        self.back_visible = False
        self.left_hand_visibility = False
        self.right_hand_visibility = False

        self.posture_abort = False
        self.bad_posture = False

        self.reps = 0

    def _use_both_hands(
        self,
        shoulder_left: tuple[int, int] | tuple[None],
        elbow_left: tuple[int, int] | tuple[None],
        wrist_left: tuple[int, int] | tuple[None],
        shoulder_right: tuple[int, int] | tuple[None],
        elbow_right: tuple[int, int] | tuple[None],
        wrist_right: tuple[int, int] | tuple[None],
    ) -> None:

        self.right_hand.update_state(
            shoulder=shoulder_right,
            elbow=elbow_right,
            wrist=wrist_right,
        )
        self.left_hand.update_state(
            shoulder=shoulder_left, elbow=elbow_left, wrist=wrist_left
        )
        self.reps = self.push_up.update_state_both_hands(
            self.right_hand, self.left_hand, self.back, self.reps
        )

    def _use_right_hand(
        self,
        shoulder_right: tuple[int, int] | tuple[None],
        elbow_right: tuple[int, int] | tuple[None],
        wrist_right: tuple[int, int] | tuple[None],
    ):

        self.right_hand.update_state(
            shoulder=shoulder_right, elbow=elbow_right, wrist=wrist_right
        )

        self.reps = self.push_up.update_state_right(
            self.right_hand, self.back, self.reps
        )

    def _use_left_hand(
        self,
        shoulder_left: tuple[int, int] | tuple[None],
        elbow_left: tuple[int, int] | tuple[None],
        wrist_left: tuple[int, int] | tuple[None],
    ):

        self.left_hand.update_state(
            shoulder=shoulder_left, elbow=elbow_left, wrist=wrist_left
        )

        self.reps = self.push_up.update_state_left(self.left_hand, self.back, self.reps)

    def update_state(
        self,
        shoulder_left: tuple[int, int] | tuple[None],
        elbow_left: tuple[int, int] | tuple[None],
        wrist_left: tuple[int, int] | tuple[None],
        shoulder_right: tuple[int, int] | tuple[None],
        elbow_right: tuple[int, int] | tuple[None],
        wrist_right: tuple[int, int] | tuple[None],
        hip_left: tuple[int, int] | tuple[None],
        hip_right: tuple[int, int] | tuple[None],
        knee_left: tuple[int, int] | tuple[None],
        knee_right: tuple[int, int] | tuple[None],
    ):
        self.left_hand_visibility = shoulder_left and elbow_left and wrist_left
        self.right_hand_visibility = shoulder_right and elbow_right and wrist_right

        self.posture_abort = self.back.update_state(
            shoulder_left, shoulder_right, hip_left, hip_right, knee_left, knee_right
        )
        self.bad_posture = not self.back.is_straight  # pylint: disable=no-member

        if self.left_hand_visibility and self.right_hand_visibility:
            self._use_both_hands(
                shoulder_left=shoulder_left,
                elbow_left=elbow_left,
                wrist_left=wrist_left,
                shoulder_right=shoulder_right,
                elbow_right=elbow_right,
                wrist_right=wrist_right,
            )
        elif self.left_hand_visibility and not self.right_hand_visibility:
            self._use_left_hand(
                shoulder_left=shoulder_left,
                elbow_left=elbow_left,
                wrist_left=wrist_left,
            )
        elif not self.left_hand_visibility and self.right_hand_visibility:
            self._use_right_hand(
                shoulder_right=shoulder_right,
                elbow_right=elbow_right,
                wrist_right=wrist_right,
            )

        return self.push_up.current_state.value, self.reps


class PushUp(StateMachine):
    none = State("none", initial=True)
    up = State("up")
    down = State("down")
    going_down = State("going_down")
    going_up = State("going_up")

    switch_init = none.to(up)
    switch_up = going_up.to(up)
    switch_down = going_down.to(down)
    switch_going_up = down.to(going_up)
    switch_going_down = up.to(going_down)

    def update_state_both_hands(
        self,
        right_hand: "Hand",
        left_hand: "Hand",
        back: "Back",
        reps: int,
    ) -> int:
        # From init state to top state
        if (
            right_hand.is_straight  # pylint: disable=no-member
            and left_hand.is_straight  # pylint: disable=no-member
            and back.is_straight  # pylint: disable=no-member
            and self.current_state.value == "none"
        ):
            self.switch_init()

        # From top state to going_down state
        if (
            right_hand.is_bent_down
            and left_hand.is_bent_down
            and back.is_straight
            and self.current_state.value == "up"
        ):
            self.switch_going_down()

        # From going_down state to floor state
        if (
            right_hand.is_contact
            and left_hand.is_contact
            and back.is_straight
            and self.current_state.value == "going_down"
        ):
            self.switch_down()

        # From floor state to going_up state
        if (
            right_hand.is_bent_up
            and left_hand.is_bent_up
            and back.is_straight
            and self.current_state.value == "down"
        ):
            self.switch_going_up()

        # From going_up state to top state
        if (
            right_hand.is_straight
            and left_hand.is_straight
            and back.is_straight
            and self.current_state.value == "going_up"
        ):
            self.switch_up()
            reps += 1

        return reps

    def update_state_left(
        self,
        left_hand: "Hand",
        back: "Back",
        reps: int,
    ) -> int:

        # From init state to top state
        if (
            left_hand.is_straight  # pylint: disable=no-member
            and back.is_straight  # pylint: disable=no-member
            and self.current_state.value == "none"
        ):
            self.switch_init()

        # From top state to going_down state
        if (
            left_hand.is_bent_down
            and back.is_straight
            and self.current_state.value == "up"
        ):
            self.switch_going_down()

        # From going_down state to floor state
        if (
            left_hand.is_contact
            and back.is_straight
            and self.current_state.value == "going_down"
        ):
            self.switch_down()

        # From floor state to going_up state
        if (
            left_hand.is_bent_up
            and back.is_straight
            and self.current_state.value == "down"
        ):
            self.switch_going_up()

        # From going_up state to top state
        if (
            left_hand.is_straight
            and back.is_straight
            and self.current_state.value == "going_up"
        ):
            self.switch_up()
            reps += 1

        return reps

    def update_state_right(
        self,
        right_hand: "Hand",
        back: "Back",
        reps: int,
    ) -> int:
        # From init state to top state
        if (
            right_hand.is_straight  # pylint: disable=no-member
            and back.is_straight  # pylint: disable=no-member
            and self.current_state.value == "none"
        ):
            self.switch_init()

        # From top state to going_down state
        if (
            right_hand.is_bent_down
            and back.is_straight
            and self.current_state.value == "up"
        ):
            self.switch_going_down()

        # From going_down state to floor state
        if (
            right_hand.is_contact
            and back.is_straight
            and self.current_state.value == "going_down"
        ):
            self.switch_down()

        # From floor state to going_up state
        if (
            right_hand.is_bent_up
            and back.is_straight
            and self.current_state.value == "down"
        ):
            self.switch_going_up()

        # From going_up state to top state
        if (
            right_hand.is_straight
            and back.is_straight
            and self.current_state.value == "going_up"
        ):
            self.switch_up()
            reps += 1

        return reps


class Hand(StateMachine):
    init = State("init state", initial=True)  # Before key point detection
    straight = State("straight")  # greater than 160 degrees
    bent_down = State("bent down")  # between 160 and 100 degrees, going down
    bent_up = State("bent up")  # between 160 and 100 degrees, going up
    contact = State("into the body")  # less than 100 degrees but above 10

    switch_init = init.to(straight)
    switch_bent_down = straight.to(bent_down)
    switch_contact = bent_down.to(contact)
    switch_bent_up = contact.to(bent_up)
    switch_straight = bent_up.to(straight)

    def update_state(
        self,
        shoulder: tuple[int, int] | tuple[None],
        elbow: tuple[int, int] | tuple[None],
        wrist: tuple[int, int] | tuple[None],
    ):

        current_angle = (
            calculate_angle_between_points(shoulder, elbow, wrist)
            if shoulder and elbow and wrist
            else 0
        )
        # Go from init state to straight state
        if current_angle > 160 and self.current_state.value == "init":
            self.switch_init()
        # Go from straight state to bent state
        elif 160 > current_angle > 100 and self.current_state.value == "straight":
            self.switch_bent_down()
        # Go from bent state to contact state
        elif 100 > current_angle > 60 and self.current_state.value == "bent_down":
            self.switch_contact()
        # Go from contact state to bent state
        elif 160 > current_angle > 100 and self.current_state.value == "contact":
            self.switch_bent_up()
        # Go from bent state to straight state
        elif current_angle > 160 and self.current_state.value == "bent_up":
            self.switch_straight()

        return self.current_state.value


class Back(StateMachine):
    init = State("init state", initial=True)  # before key point detection
    straight = State("straight")
    bent = State("bent")

    switch_init = init.to(straight)
    switch_bent = straight.to(bent)
    switch_straight = bent.to(straight)

    def update_state(
        self,
        shoulder_left: tuple[int, int] | tuple[None],
        shoulder_right: tuple[int, int] | tuple[None],
        hip_left: tuple[int, int] | tuple[None],
        hip_right: tuple[int, int] | tuple[None],
        knee_left: tuple[int, int] | tuple[None],
        knee_right: tuple[int, int] | tuple[None],
    ):
        angle_left_back = (
            calculate_angle_between_points(shoulder_left, hip_left, knee_left)
            if shoulder_left and hip_left and knee_left
            else 0
        )
        angle_right_back = (
            calculate_angle_between_points(shoulder_right, hip_right, knee_right)
            if shoulder_right and hip_right and knee_right
            else 0
        )

        lower = 160
        upper = 180
        error = 10

        # Check if either/or back angles are close to 180 degrees +- 20
        # In initial state -> straight
        if self.current_state.value == "init" and (
            (lower <= angle_left_back <= upper) or (lower <= angle_right_back <= upper)
        ):
            self.switch_init()
        # Skip if no back visibility
        elif angle_left_back == 0 and angle_right_back == 0:
            # Abort update if no back points are available
            print("No back visibility, Counting reps, but posture has no estimate")
            if self.current_state.value == "bent":
                # Force state into straight when no knees are visible
                self.switch_straight()
        # In state straight -> bent
        elif self.current_state.value == "straight" and (
            (error < angle_left_back < lower or angle_left_back > upper)
            or (error < angle_right_back < lower or angle_right_back > upper)
        ):
            self.switch_bent()
        # In state bent -> straight
        elif self.current_state.value == "bent" and (
            (lower <= angle_left_back <= upper) or (lower <= angle_right_back < upper)
        ):
            self.switch_straight()

        return angle_left_back == 0 and angle_right_back == 0


if __name__ == "__main__":
    print("ha loh")
