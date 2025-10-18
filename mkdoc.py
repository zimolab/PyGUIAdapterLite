import shlex
import subprocess
import sys

if __name__ == "__main__":
    action = sys.argv[1]
    py = sys.executable
    command = [py]
    if action == "toc":
        command.extend(
            [
                "tools/mktoc.py",
                "--placeholder",
                "[TOC]",
                "README_draft.md",
                "-o",
                "README.md",
            ]
        )
    elif action == "typedoc":
        command.extend(
            ["tools/mktypedoc.py", "--action", "save", "--output-file", "tmp.md"]
        )
    else:
        print("Invalid action")
        sys.exit(1)
    print("Running command: ", shlex.join(command))
    sys.exit(subprocess.call(command))
