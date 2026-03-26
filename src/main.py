from analyzer import Results
from lib import uniform, weighted
from trees import (
    Bending,
    BigJungle,
    BrownMushroom,
    Cherry,
    DarkOak,
    Forking,
    Fungus,
    Giant,
    Mangrove,
    MangroveVariant,
    RedMushroom,
    Straight,
    Tree,
)


def main():
    trees: dict[str, Tree] = {
        "Oak": Straight(4, 2, 0),
        "Spruce": Straight(5, 2, 1),
        "Birch": Straight(5, 2, 0),
        "Jungle": Straight(4, 8, 0),
        "Acacia": Forking(5, 2, 2),
        "Azalea": Bending(4, 2, 0, uniform(1, 2)),
        "Mangrove": Mangrove(
            0.85,
            MangroveVariant(2, 1, 4, uniform(1, 4), 0.5, uniform(0, 1)),
            MangroveVariant(4, 1, 9, uniform(1, 6), 0.5, uniform(0, 1)),
        ),
        "Cherry": Cherry(
            7,
            1,
            0,
            weighted({1: 1, 2: 1, 3: 1}),
            uniform(2, 4),
            uniform(-4, -3),
            uniform(-1, 0),
        ),
        #
        "Big Spruce": Giant(13, 2, 14),
        "Big Jungle": BigJungle(10, 2, 19),
        "Dark Oak": DarkOak(6, 2, 1),
        "Pale Oak": DarkOak(6, 2, 1),
        #
        "Brown Mushroom": BrownMushroom(3),
        "Red Mushroom": RedMushroom(2),
        "Huge Fungus": Fungus(),
    }

    for name, tree in trees.items():
        print(f"{name}: {Results(tree)}")


if __name__ == "__main__":
    main()
