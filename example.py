"""
Beginner examples of subprocess.run, the standard way to run an external
command from Python and (optionally) capture what it prints.

Each example is a small function you can read top to bottom. Run this file
directly to see them all execute:

    python3 example.py
"""

import subprocess


def example_basic_run():
    """Run a command and let its output go straight to the terminal."""
    result = subprocess.run(["echo", "hello from a subprocess"])
    # result.returncode is 0 when the command succeeded.
    assert result.returncode == 0


def example_capture_output():
    """Capture stdout/stderr as strings instead of printing them."""
    result = subprocess.run(
        ["echo", "captured text"],
        capture_output=True,  # fills in result.stdout / result.stderr
        text=True,  # decode bytes to str (otherwise you get bytes)
    )
    print("stdout was:", result.stdout.strip())
    assert result.stdout.strip() == "captured text"


def example_check_returncode_manually():
    """By default, a failing command does NOT raise - you check it yourself."""
    result = subprocess.run(["ls", "/no/such/directory"], capture_output=True, text=True)
    if result.returncode != 0:
        print("command failed, stderr was:", result.stderr.strip())
    assert result.returncode != 0


def example_check_true_raises():
    """With check=True, a non-zero exit code raises CalledProcessError."""
    try:
        subprocess.run(["ls", "/no/such/directory"], capture_output=True, text=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"caught expected error: exit code {e.returncode}")
        return
    raise AssertionError("expected CalledProcessError")


def example_list_args_not_shell_string():
    """
    Pass the command as a list of arguments (the safe default), not a single
    shell string. This avoids shell-injection bugs when arguments contain
    user input, and you don't need shell=True.
    """
    filename = "some file; rm -rf /"  # a hostile-looking filename, still just a string here
    result = subprocess.run(["echo", "searching for:", filename], capture_output=True, text=True)
    assert filename in result.stdout


def example_cwd():
    """Run the command in a specific working directory with cwd=."""
    result = subprocess.run(["pwd"], cwd="/tmp", capture_output=True, text=True)
    assert result.stdout.strip() == "/tmp"


def example_env():
    """Pass a custom environment to the subprocess with env=."""
    result = subprocess.run(
        ["printenv", "GREETING"],
        capture_output=True,
        text=True,
        env={"GREETING": "hi there"},
    )
    assert result.stdout.strip() == "hi there"


def example_timeout():
    """Kill a command that runs too long using timeout= (seconds)."""
    try:
        subprocess.run(["sleep", "5"], timeout=0.5)
    except subprocess.TimeoutExpired:
        print("command timed out, as expected")
        return
    raise AssertionError("expected TimeoutExpired")


def example_send_stdin():
    """Send data to the command's stdin with input=."""
    result = subprocess.run(["cat"], input="piped in through stdin\n", capture_output=True, text=True)
    assert result.stdout == "piped in through stdin\n"


if __name__ == "__main__":
    examples = [
        example_basic_run,
        example_capture_output,
        example_check_returncode_manually,
        example_check_true_raises,
        example_list_args_not_shell_string,
        example_cwd,
        example_env,
        example_timeout,
        example_send_stdin,
    ]
    for example in examples:
        print(f"\n--- {example.__name__} ---")
        example()
    print("\nAll examples ran successfully.")
