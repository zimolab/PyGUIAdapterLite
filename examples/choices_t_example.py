from pyguiadapterlite import uprint, GUIAdapter
from pyguiadapterlite.types import choices_t, MultiChoiceValue


def choices_t_example(arg1: choices_t, arg2: choices_t):
    uprint(f"arg1: {arg1}, len: {len(arg1)}")
    uprint(f"arg2: {arg2}, len: {len(arg2)}")


if __name__ == "__main__":
    adapter = GUIAdapter()
    adapter.add(
        choices_t_example,
        arg1=MultiChoiceValue(
            label="Select Languages",
            choices=[
                "Python",
                "Java",
                "Kotlin",
                "C++",
                "C#",
                "Ruby",
                "JavaScript",
                "PHP",
            ],
            default_value=["Python", "Kotlin", "C++", "C#"],
            columns=3,
        ),
        arg2=MultiChoiceValue(
            label="Frameworks",
            choices=[
                "Django",
                "Flask",
                "Spring",
                "Laravel",
                "Symfony",
                "Zend",
                "Ruby on Rails",
            ],
            default_value=["Django", "Flask", "Laravel"],
            columns=2,
            content_title="Popular Frameworks",
            hide_label=False,
        ),
    )
    adapter.run()
