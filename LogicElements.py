import pygame.image

import assets


class Gate:

    all_gates = []

    def __init__(self, max_inputs: int, is_inverted=False):
        self.textures = []
        self.max_inputs = max_inputs
        self.inputs = []
        self.masters = []
        while len(self.inputs) < self.max_inputs:
            self.inputs.append(None)

        self.internal_state = is_inverted
        self.external_state = is_inverted
        self.is_inverted = is_inverted

        self.textures = [pygame.image.load(assets.resource_path("none.png")), pygame.image.load(assets.resource_path("none.png"))]

        Gate.all_gates.append(self)

    def calculate_output(self):
        self.internal_state = self.is_inverted

    def send_output(self):
        self.external_state = self.internal_state

    def check_for_any_connections(self):
        has_any = False
        for input in self.inputs:
            if input is not None:
                has_any = True
        return has_any

    def connect(self, other, port):
        if isinstance(other, Pin):
            if not other.has_input:
                return 1
        other.inputs[port] = self

    def disconnect(self, port):
        self.inputs[port] = None

    def delete(self):
        i = 0
        while i < len(self.inputs):
            self.disconnect(i)
            i = i + 1

        for gate in Gate.all_gates:
            i = 0
            while i < gate.max_inputs:
                if gate.inputs[i] == self.masters:
                    gate.disconnect(i)
                i = i + 1
        if self in Gate.all_gates:
            Gate.all_gates.remove(self)

    @classmethod
    def in_tick(cls):
        for gate in cls.all_gates:
            gate.calculate_output()

    @classmethod
    def out_tick(cls):
        for gate in cls.all_gates:
            gate.send_output()


class ANDGate(Gate):

    def __init__(self, max_inputs: int, is_inverted: bool):
        super().__init__(max_inputs, is_inverted)
        self.textures = [pygame.image.load(assets.resource_path("and.png")).convert_alpha(), pygame.image.load(assets.resource_path("nand.png"))]

    def calculate_output(self):
        if self.check_for_any_connections():
            self.internal_state = not self.is_inverted
            for input in self.inputs:
                if isinstance(input, Gate):
                    if not input.external_state:
                        self.internal_state = self.is_inverted
                        return 0
        else:
            self.internal_state = self.is_inverted


class ORGate(Gate):

    def __init__(self, max_inputs: int, is_inverted=False):
        super().__init__(max_inputs, is_inverted)
        self.textures = [pygame.image.load(assets.resource_path("or.png")).convert_alpha(), pygame.image.load(assets.resource_path("nor.png"))]

    def calculate_output(self):
        self.internal_state = self.is_inverted
        if self.check_for_any_connections():
            for input in self.inputs:
                if isinstance(input, Gate):
                    if input.external_state:
                        self.internal_state = not self.is_inverted
                        return 0



class Buffer(Gate):

    def __init__(self, is_inverted=False):
        super().__init__(1, is_inverted)
        self.textures = [pygame.image.load(assets.resource_path("buffer.png")).convert_alpha(), pygame.image.load(assets.resource_path("not.png"))]

    def calculate_output(self):
        if self.check_for_any_connections():
            if self.is_inverted:
                self.internal_state = not self.inputs[0].external_state
            else:
                self.internal_state = self.inputs[0].external_state
        else:
            self.internal_state = self.is_inverted


class Pin(Buffer):
    
    def __init__(self, is_built_in=False, has_input=True, has_output=True):
        super().__init__(is_inverted=False)

        self.is_built_in = is_built_in

        self.has_output = has_output
        self.has_input = has_input

        self.textures = [pygame.image.load(assets.resource_path("none.png")), pygame.image.load(assets.resource_path("none.png"))]
    
    def connect(self, other, port):
        if self.has_output:
            super().connect(other, port)
    
    def calculate_output(self):
        if self.has_input:
            super().calculate_output()


class FlipFlop(Gate):

    def __init__(self, inputs: int, is_rising_edge=True):
        super().__init__(max_inputs=inputs, is_inverted=False)

        self.is_rising_edge = is_rising_edge
        self.previous_clock = False

    def change_previous_clock(self):
        if isinstance(self.inputs[2], Gate):
            self.previous_clock = self.inputs[2].external_state
        else:
            self.previous_clock = False

    def check_clock(self):
        if isinstance(self.inputs[2], Gate):
            if self.inputs[2].external_state != self.previous_clock and self.inputs[2].external_state == self.is_rising_edge:
                return True
            else:
                return False
        return False


class DFlipFlop(FlipFlop):

    def __init__(self, is_rising_edge=True):
        super().__init__(4, is_rising_edge)

        self.textures = [pygame.image.load(assets.resource_path("D.png")), pygame.image.load(assets.resource_path("D.png"))]

    def calculate_output(self):
        if self.check_clock():

            if self.inputs[1] is None:
                self.internal_state = False
            else:
                self.internal_state = self.inputs[1].external_state

        if isinstance(self.inputs[0], Gate) and not self.inputs[0].external_state:
            self.internal_state = False

        if isinstance(self.inputs[3], Gate) and not self.inputs[3].external_state:
            self.internal_state = True

        self.change_previous_clock()


class JKFlipFlop(FlipFlop):

    def __init__(self, is_rising_edge=True):
        super().__init__(5, is_rising_edge)

        self.textures = [pygame.image.load(assets.resource_path("JK.png")), pygame.image.load(assets.resource_path("JK.png"))]

    def calculate_output(self):
        if self.check_clock():

            if not self.internal_state and isinstance(self.inputs[1], Gate) and self.inputs[1].external_state:
                self.internal_state = True
            elif self.internal_state and isinstance(self.inputs[3], Gate) and self.inputs[3].external_state:
                self.internal_state = False

        if isinstance(self.inputs[0], Gate) and not self.inputs[0].external_state:
            self.internal_state = False

        if isinstance(self.inputs[4], Gate) and not self.inputs[4].external_state:
            self.internal_state = True

        self.change_previous_clock()


class HiddenBuffer(Buffer):

    def disconnect(self, port):
        return
