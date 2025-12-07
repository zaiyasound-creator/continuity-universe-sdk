class Color:
    @staticmethod
    def rgb(r: int, g: int, b: int) -> int:
        """Convert RGB to nearest ANSI 256-color code."""
        r = int(r / 51)
        g = int(g / 51)
        b = int(b / 51)
        return 16 + 36 * r + 6 * g + b

    @staticmethod
    def wrap(text: str, r: int, g: int, b: int) -> str:
        code = Color.rgb(r, g, b)
        return f"\033[38;5;{code}m{text}\033[0m"
