class Item:
    def __init__(self, left: str, right: list) -> None:
        self.left: str = left
        self.right: list = right

    def __repr__(self) -> str:
        return f'{self.left} -> {self.right}'
