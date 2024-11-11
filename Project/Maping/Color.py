def getColor(color: str) -> str:
    base: str = "\033[38;5;"
    end: str = "m"
    if color == "red":
        colour: str = "01"
    elif color == "green":
        colour: str = "02"
    elif color == "yellow":
        colour: str = "03"
    elif color == "marineBlue":
        colour: str = "04"
    elif color == "purple":
        colour: str = "05"
    elif color == "skyBlue":
        colour: str = "06"
    elif color == "gray":
        colour: str = "08"
    elif color == "lightred":
        colour: str = "09"
    else:
        colour: str = "07"  # white
    return base + colour + end
