class Item:
    def __init__(self, left: str, right: list) -> None:
        self.left: str = left
        self.right: list = right

    def __repr__(self) -> str:
        string = self.left + ' →'
        for char in self.right:
            actual = '*' if char == '.' else char
            string += ' ' + actual

        return string
