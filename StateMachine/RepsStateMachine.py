from statemachine import StateMachine, State

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
            print(self.current_state)
        elif my_angle > 160 and self.current_state.value == "ReturnState3":
            self.to_initial()
            counter += 1
            print(self.current_state.value)

        if 160 > my_angle > 100 and self.current_state.value == "State1":
            self.switch2()
            print(self.current_state.value)
        if 160 > my_angle > 100 and self.current_state.value == "ReturnState2":
            self.switch5()
            print(self.current_state.value)

        if 100 > my_angle > 60 and self.current_state.value == "State2":
            self.switch3()
            print(self.current_state.value)
        elif 100 > my_angle > 60 and self.current_state.value == "ReturnState1":
            self.switch4()
            print(self.current_state.value)

        if my_angle < 40 and stage == "down" and self.current_state.value == "State3":
            stage = "up"

            self.start_return_to_init_state()
            print(self.current_state.value)

        return stage, counter, self.current_state.value
class PushUp(StateMachine):
    State0 = State("init state", initial=True) # before key point detection
    State1 = State("base state")                # detect min, max, straight hands and legs, everything be visible
    State2 = State("moving down")               # about 120 degrees
    State3 = State("down")                      # less than 60 degrees

    ReturnState1 = State("moving up")           # more than 60 degrees
    ReturnState2 = State("return_third_quadrant")   # more than 120 degrees
    ReturnState3 = State("return_second_quadrant")  # finished, return to base state

    switch1 = State0.to(State1)
    switch2 = State1.to(State2)
    switch3 = State2.to(State3)
    start_return_to_init_state = State3.to(ReturnState1)

    switch4 = ReturnState1.to(ReturnState2)
    switch5 = ReturnState2.to(ReturnState3)

    to_initial = ReturnState3.to(State0)


