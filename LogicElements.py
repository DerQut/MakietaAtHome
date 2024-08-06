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

        self.textures = [pygame.image.load(assets.resource_path("assets/none.png")), pygame.image.load(assets.resource_path("assets/none.png"))]

        Gate.all_gates.append(self)

    def calculate_output(self):
        self.internal_state = self.is_inverted

    def send_output(self):
        self.external_state = self.internal_state ^ self.is_inverted

    def check_for_any_connections(self):
        for gate in self.inputs:
            if isinstance(gate, Gate):
                return True
        return False

    def connect(self, other, port: int):
        if isinstance(other, Pin):
            if not other.has_input:
                return 1
        other.inputs[port] = self

    def disconnect(self, port: int):
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
        self.textures = [pygame.image.load(assets.resource_path("assets/and.png")).convert_alpha(), pygame.image.load(assets.resource_path("assets/nand.png"))]

    def calculate_output(self):

        if not self.check_for_any_connections():
            self.internal_state = False
            return -1

        self.internal_state = True
        for gate in self.inputs:
            if isinstance(gate, Gate):
                if not gate.external_state:
                    self.internal_state = False
                    return 0
        return 1


class ORGate(Gate):

    def __init__(self, max_inputs: int, is_inverted=False):
        super().__init__(max_inputs, is_inverted)
        self.textures = [pygame.image.load(assets.resource_path("assets/or.png")).convert_alpha(), pygame.image.load(assets.resource_path("assets/nor.png"))]

    def calculate_output(self):
        self.internal_state = False
        if not self.check_for_any_connections():
            return -1

        for gate in self.inputs:
            if isinstance(gate, Gate):
                if gate.external_state:
                    self.internal_state = True
                    return 1
        return 0


class Buffer(Gate):

    def __init__(self, is_inverted=False):
        super().__init__(1, is_inverted)
        self.textures = [pygame.image.load(assets.resource_path("assets/buffer.png")).convert_alpha(), pygame.image.load(assets.resource_path("assets/not.png"))]

    def calculate_output(self):
        if not self.check_for_any_connections():
            self.internal_state = False
            return -1

        self.internal_state = self.inputs[0].external_state
        return 0


class Pin(Buffer):
    
    def __init__(self, is_built_in=False, has_input=True, has_output=True):
        super().__init__(is_inverted=False)

        self.is_built_in = is_built_in

        self.has_output = has_output
        self.has_input = has_input

        self.textures = [pygame.image.load(assets.resource_path("assets/none.png")), pygame.image.load(assets.resource_path("assets/none.png"))]
    
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
        return True


class DFlipFlop(FlipFlop):

    def __init__(self, is_rising_edge=True):
        super().__init__(4, is_rising_edge)

        self.textures = [pygame.image.load(assets.resource_path("assets/D.png")), pygame.image.load(assets.resource_path("assets/D.png"))]

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

        self.textures = [pygame.image.load(assets.resource_path("assets/JK.png")), pygame.image.load(assets.resource_path("assets/JK.png"))]

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

    def calculate_output(self):
        super().calculate_output()
        gate = self.inputs[0]
        if isinstance(gate, JKFlipFlop):
            if isinstance(gate.inputs[0], Gate) and isinstance(gate.inputs[4], Gate):
                if (not gate.inputs[0].external_state) and (not gate.inputs[4].external_state):
                    self.internal_state = False
        elif isinstance(gate, DFlipFlop):
            if isinstance(gate.inputs[0], Gate) and isinstance(gate.inputs[3], Gate):
                if (not gate.inputs[0].external_state) and (not gate.inputs[3].external_state):
                    self.internal_state = False
