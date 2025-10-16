from pyguiadapterlite import uprint, GUIAdapter


# step 0: define your function, here are some important points:
# - annotate the parameters with their types using Python's type hints syntax
# the GUIAdapter will automatically generate widgets for each parameter based on their types(by default)
# - you can give the parameter a default value, the value will be used as the initial value of its widget
def basic_types_demo(
    int_value: int = 10,
    float_value: float = 3.14,
    str_value: str = "Hello, world!",
    bool_value: bool = True,
):
    # uprint() is a function which is very similar to the built-in print()
    # the difference is that it will not print the output to the stdout, instead,
    # it will print it to the output area of the execute window
    uprint("int_value:", int_value)
    uprint("float_value:", float_value)
    uprint("str_value:", str_value)
    uprint("bool_value:", bool_value)
    # you can return a value like any other function.
    # this value will be captured by the execute window
    # by default, the value will be printed to the output area
    # and a popup window will be shown to display the value.
    return "Function Done!"


if __name__ == "__main__":
    # step 1: create a GUIAdapter instance
    adapter = GUIAdapter()
    # step 2: add your function to the adapter
    adapter.add(basic_types_demo)
    # step 3: run the adapter,
    adapter.run()
