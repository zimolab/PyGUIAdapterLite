import time

from pyguiadapterlite import GUIAdapter, uprint, is_function_cancelled
from pyguiadapterlite import (
    is_progressbar_enabled,
    is_progress_label_enabled,
    start_progressbar,
    update_progressbar,
    stop_progressbar,
)


def progressbar_demo(delay: int = 1000, hide_after_stop: bool = True):
    # Check if progressbar and progress label are enabled
    progressbar_enabled = is_progressbar_enabled()
    progress_label_enabled = is_progress_label_enabled()
    uprint("is progressbar enabled:", progressbar_enabled)
    uprint("is progress label enabled:", progress_label_enabled)

    # initialize progressbar
    start_progressbar(total=100, initial_value=0, initial_msg="Starting...")
    cancelled = False
    for i in range(100):
        current_progress = i
        # check if user clicked the cancel button
        # if so, quit the loop and update the progressbar
        if is_function_cancelled():
            update_progressbar(current_progress, "Cancelling...")
            # delay for a while to mock the cancellation process
            time.sleep(delay / 1000)
            cancelled = True
            break
        # update progress of the progressbar and the progress label
        update_progressbar(i + 1, f"Progress: {i+1}%")
        current_progress += 1
        # delay for a while to mock some heavy work
        time.sleep(delay / 1000)

    if cancelled:
        update_progressbar(0, "Task Cancelled!")
    # stop the progressbar and update the progress label
    # when hide_after_stop=False to keep the progressbar visible after the function returned
    # otherwise, the progressbar will disappear after the function returned
    stop_progressbar(hide_after_stop=hide_after_stop)


if __name__ == "__main__":
    adapter = GUIAdapter()
    # progressbar and progress label are not enabled by default
    # you can enable them with a window_config object where
    # the enable_progressbar and enable_progress_label fields are set to True
    # or just pass enable_progressbar and enable_progress_label as arguments as shown below
    adapter.add(
        progressbar_demo,
        cancelable=True,
        enable_progressbar=True,
        enable_progress_label=True,
    )
    adapter.run()
