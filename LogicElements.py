class Cable:

    def __init__(self):
        self.is_on = False
        self.end_point = (None, None)

    def disconnect(self):
        if isinstance(self.end_point[0], Gate):
            self.end_point[0].inputs[self.end_point[1]] = None
            self.end_point = (None, None)


class Gate:

    all_gates = []

    def __init__(self, max_inputs, is_inverted=False):
        self.max_inputs = max_inputs
        self.inputs = []
        while len(self.inputs) < self.max_inputs:
            self.inputs.append(None)

        self.is_on = is_inverted
        self.is_inverted = is_inverted
        self.output = Cable()

        Gate.all_gates.append(self)

    def calculate_output(self):
        self.is_on = self.is_inverted

    def send_output(self):
        self.output.is_on = self.is_on

    def check_for_any_connections(self):
        has_any = False
        for input in self.inputs:
            if input is not None:
                has_any = True
        return has_any

    def connect(self, other, port):
        self.output.end_point = (other, port)
        other.inputs[port] = self.output

    @classmethod
    def in_tick(cls):
        for gate in cls.all_gates:
            gate.calculate_output()

    @classmethod
    def out_tick(cls):
        for gate in cls.all_gates:
            gate.send_output()


class ANDGate(Gate):

    def calculate_output(self):
        if self.check_for_any_connections():
            self.is_on = not self.is_inverted
            for input in self.inputs:
                if isinstance(input, Cable):
                    if not input.is_on:
                        self.is_on = self.is_inverted
                        break
        else:
            self.is_on = self.is_inverted


class ORGate(Gate):

    def calculate_output(self):
        if self.check_for_any_connections():
            self.is_on = not self.is_inverted
            for input in self.inputs:
                if isinstance(input, Cable):
                    if input.is_on:
                        self.is_on = not self.is_inverted
                        return 0

        self.is_on = self.is_inverted


class Buffer(Gate):

    def __init__(self, is_inverted=False):
        super().__init__(1, is_inverted)

    def calculate_output(self):
        for input in self.inputs:
            if isinstance(input, Cable):
                if not self.is_inverted:
                    self.is_on = input.is_on
                else:
                    self.is_on = not input.is_on
            else:
                self.is_on = self.is_inverted
