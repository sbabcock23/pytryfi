class ledColors(object):
    def __init__(self, ledColorCode, hexCode, name):
        self._ledColorCode = ledColorCode
        self._hexCode = hexCode
        self._name = name
    
    def __str__(self):
        return f"Color: {self.name} Hex Code: {self.hexCode} Color Code: {self.ledColorCode}"
    
    @property
    def name(self):
        return self._name
    @property
    def ledColorCode(self):
        return self._ledColorCode
    @property
    def hexCode(self):
        return self._hexCode