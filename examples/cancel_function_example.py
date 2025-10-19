import time

from pyguiadapterlite import uprint, is_function_cancelled, GUIAdapter


def mock_heavy_task(mount: int = 100, delay: float = 0.05):
    uprint("Starting heavy task...")
    cancelled = False
    total = 0
    for i in range(mount):
        if is_function_cancelled():
            uprint("User asked to cancel the task.")
            cancelled = True
            break
        total += i
        uprint(f"Progress: {i+1}/{mount}")
        time.sleep(delay)

    if cancelled:
        uprint("Task cancelled by user.")
        return -1
    uprint("Task completed successfully.")
    return total


if __name__ == "__main__":
    adapter = GUIAdapter()
    adapter.add(mock_heavy_task, cancelable=True)
    adapter.run()
