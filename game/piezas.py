class Pieza:

    def __init__(self, tipo, color):
        self.tipo = tipo      # peon, torre, etc
        self.color = color    # blanca / oscura

    def __repr__(self):
        return f"{self.tipo[0]}{self.color[0]}"