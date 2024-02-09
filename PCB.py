import LogicElements


class PCB:

    def __init__(self, size):

        self.size = size

        self.all_components = []


class Component:

    def __init__(self, pcb, position, size, logic_element):

        self.pcb = pcb
        self.position = position
        self.size = size

        self.logic_element = logic_element

        self.pcb.all_components.append(self)
