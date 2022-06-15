from sys import path
from pathlib import Path
from unittest import main


if __name__ == "__main__":
    path.append(Path(__file__).parent.parent.__str__())
    from image import *

    main()