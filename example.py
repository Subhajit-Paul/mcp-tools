"""
Beginner examples of subprocess.run, the standard way to run an external
command from Python and (optionally) capture what it prints.

Each tool below demonstrates one subprocess.run pattern. Run this file as an
MCP server like the other tools in this repo:

    fastmcp run example.py:mcp --transport sse --host 127.0.0.1 --port 6970

Or just run it directly to execute every demo once and print the results:

    python3 example.py
"""

import subprocess

from fastmcp import FastMCP

mcp = FastMCP(name="SubprocessExamplesServer")


@mcp.tool
def demo_capture_output() -> str:
    """
    Runs a command and captures its stdout instead of letting it print
    straight to the terminal.

    Returns:
        str: The captured stdout, decoded to text.

    Example:
        >>> demo_capture_output()
        'captured text'
    """
    result = subprocess.run(
        ["echo", "captured text"],
        capture_output=True,  # fills in result.stdout / result.stderr
        text=True,  # decode bytes to str (otherwise you get bytes)
    )
    return result.stdout.strip()


@mcp.tool
def demo_check_returncode() -> str:
    """
    Runs a failing command. By default subprocess.run does NOT raise on a
    non-zero exit code - you check result.returncode yourself.

    Returns:
        str: A message reporting the exit code and stderr.

    Example:
        >>> demo_check_returncode()
        'exit code 2, stderr: ls: cannot access ... No such file or directory'
    """
    result = subprocess.run(["ls", "/no/such/directory"], capture_output=True, text=True)
    return f"exit code {result.returncode}, stderr: {result.stderr.strip()}"


@mcp.tool
def demo_check_true_raises() -> str:
    """
    Runs the same failing command, but with check=True so subprocess raises
    CalledProcessError instead of returning a non-zero result.

    Returns:
        str: A message confirming the exception was caught.

    Example:
        >>> demo_check_true_raises()
        'caught CalledProcessError with exit code 2'
    """
    try:
        subprocess.run(["ls", "/no/such/directory"], capture_output=True, text=True, check=True)
    except subprocess.CalledProcessError as e:
        return f"caught CalledProcessError with exit code {e.returncode}"
    return "command unexpectedly succeeded"


@mcp.tool
def demo_list_args_not_shell_string() -> str:
    """
    Passes the command as a list of arguments (the safe default) instead of
    a single shell string, so arguments are never re-interpreted by a shell.
    This avoids shell-injection bugs when arguments contain user input.

    Returns:
        str: The captured stdout, showing the hostile-looking argument was
             treated as plain text, not executed.

    Example:
        >>> demo_list_args_not_shell_string()
        'searching for: some file; rm -rf /'
    """
    filename = "some file; rm -rf /"  # a hostile-looking argument, still just a string here
    result = subprocess.run(["echo", "searching for:", filename], capture_output=True, text=True)
    return result.stdout.strip()


@mcp.tool
def demo_cwd() -> str:
    """
    Runs a command in a specific working directory using cwd=, instead of
    changing directory in the current Python process.

    Returns:
        str: The working directory the command reported.

    Example:
        >>> demo_cwd()
        '/tmp'
    """
    result = subprocess.run(["pwd"], cwd="/tmp", capture_output=True, text=True)
    return result.stdout.strip()


@mcp.tool
def demo_env() -> str:
    """
    Runs a command with a custom environment passed via env=, instead of the
    parent process's environment.

    Returns:
        str: The value the subprocess read from its environment.

    Example:
        >>> demo_env()
        'hi there'
    """
    result = subprocess.run(
        ["printenv", "GREETING"],
        capture_output=True,
        text=True,
        env={"GREETING": "hi there"},
    )
    return result.stdout.strip()


@mcp.tool
def demo_timeout() -> str:
    """
    Runs a command that sleeps for 5 seconds but caps it with timeout=0.5,
    so subprocess kills it and raises TimeoutExpired.

    Returns:
        str: A message confirming the timeout fired.

    Example:
        >>> demo_timeout()
        'command timed out after 0.5s, as expected'
    """
    try:
        subprocess.run(["sleep", "5"], timeout=0.5)
    except subprocess.TimeoutExpired:
        return "command timed out after 0.5s, as expected"
    return "command unexpectedly finished in time"


@mcp.tool
def demo_send_stdin() -> str:
    """
    Sends data to a command's stdin using input=, instead of writing to a
    file or piping from the shell.

    Returns:
        str: Whatever the command echoed back from stdin.

    Example:
        >>> demo_send_stdin()
        'piped in through stdin'
    """
    result = subprocess.run(["cat"], input="piped in through stdin\n", capture_output=True, text=True)
    return result.stdout.strip()


if __name__ == "__main__":
    demos = [
        demo_capture_output,
        demo_check_returncode,
        demo_check_true_raises,
        demo_list_args_not_shell_string,
        demo_cwd,
        demo_env,
        demo_timeout,
        demo_send_stdin,
    ]
    for demo in demos:
        # .fn unwraps the underlying function from the @mcp.tool wrapper
        print(f"\n--- {demo.name} ---")
        print(demo.fn())
