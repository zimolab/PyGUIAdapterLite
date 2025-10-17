from pyguiadapterlite import uprint, GUIAdapter
from pyguiadapterlite.types import choices_t

ALL_CHOICES = (
    "Choice 1",
    "Choice 2",
    "Choice 3",
    "Choice 4",
    "Choice 5",
    "Choice 6",
)


def choices_t_example(arg: choices_t = ALL_CHOICES):
    uprint(f"You selected {len(arg)} options")
    if arg:
        uprint(f"The options are: {arg}")


if __name__ == "__main__":
    adapter = GUIAdapter()
    adapter.add(choices_t_example)
    adapter.run()
