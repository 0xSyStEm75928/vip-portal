class Neon:
    RESET   = "\033[0m"
    CYAN    = "\033[38;2;0;243;255m"
    GREEN   = "\033[38;2;50;255;50m"
    RED     = "\033[38;2;255;50;50m"
    MAGENTA = "\033[38;2;255;0;127m"

    @staticmethod
    def print_status(tag, msg, color=CYAN):
        print(f"{color}[{tag}]{Neon.RESET} {msg}")
