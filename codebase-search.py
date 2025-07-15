from fastmcp import FastMCP
import subprocess

mcp = FastMCP(name="CodebaseSearchServer")
    
@mcp.tool
def search_in_specific_file(path: str, pattern: str, file: str) -> str:
    """
    Performs a search in the specified repository path for a given pattern 
    within a specific file.

    Args:
        path (str): Path to the repository root.
        pattern (str): The search string or regex pattern.
        file (str): The file name (relative to repo root) to search within.

    Returns:
        str: Matching lines containing the pattern in the given file. 
             Returns 'Error Occurred' if the command fails.

    Example:
        >>> search_in_specific_file("/my/repo", "clk", "design.sv")
        'design.sv:12: input wire clk;\ndesign.sv:45: always @(posedge clk) ...'
    """
    try:
        result = subprocess.run(
            [f"cd {path} &&", "git", "grep", pattern, file],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        return e.stdout if e.stdout else 'Error Occurred'

@mcp.tool
def get_directory_tree(path: str) -> str:
    """
    Generates the directory tree structure of the specified repository path.

    Args:
        path (str): Path to the repository root.

    Returns:
        str: A formatted string representing the directory tree. 
             Returns 'Error Occurred' if the command fails.

    Example:
        >>> get_directory_tree("/my/repo")
        '.\n├── design\n│   ├── alu.sv\n│   └── regfile.sv\n└── tb\n    └── tb_top.sv'
    """
    try:
        result = subprocess.run(
            [f"cd {path} &&", "tree"],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        return e.stdout if e.stdout else 'Error Occurred'
    
@mcp.tool
def search_in_specific_file_with_context(path: str, pattern: str, context_lines: int, file: str = '') -> str:
    """
    Performs a search in the specified repository path for a given pattern, 
    optionally within a specific file, including a number of context lines before and after matches.

    Args:
        path (str): Path to the repository root.
        pattern (str): The search string or regex pattern.
        context_lines (int): Number of context lines before and after each match.
        file (str, optional): Specific file to search in. Defaults to searching the entire repo.

    Returns:
        str: Matching lines with the requested context. 
             Returns 'Error Occurred' if the command fails.

    Example:
        >>> search_in_specific_file_with_context("/my/repo", "reset", 2, "design.sv")
        'design.sv-44-  if (!reset)\ndesign.sv:45:      counter <= 0;\ndesign.sv-46-  else begin ...'
    """

    try:
        result = subprocess.run(
            [f"cd {path} &&", "git", "grep", f"-C{context_lines}", pattern, file],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        return e.stdout if e.stdout else 'Error Occurred'
    
@mcp.tool
def list_all_signals(path: str, file: str = "") -> str:
    """
    Extracts all signal names (wires, regs, logic, inputs, outputs) from SystemVerilog/Verilog files 
    using regex search via git grep.

    Args:
        path (str): Path to the repository root.
        file (str, optional): Specific file to search in. Defaults to entire repo.

    Returns:
        str: List of extracted signal declarations.

    Example:
        >>> list_all_signals("/my/repo", "design.sv")
        'design.sv: wire clk;\ndesign.sv: logic [3:0] counter;\n...'
    """
    try:
        patterns = r"(wire|reg|logic|input|output)\s"
        result = subprocess.run(
            [f"cd {path} &&", "git", "grep", "-E", patterns, file],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        return e.stdout if e.stdout else 'No signals found.'


@mcp.tool
def find_signal_usage(path: str, signal: str) -> str:
    """
    Finds all occurrences of a specific signal in the repository.

    Args:
        path (str): Path to the repository root.
        signal (str): Signal name to search for.

    Returns:
        str: List of lines where the signal is used.

    Example:
        >>> find_signal_usage("/my/repo", "clk")
        'design.sv: always @(posedge clk) ...\nmodule_tb.sv: clk = 0;\n...'
    """
    try:
        result = subprocess.run(
            [f"cd {path} &&", "git", "grep", "-n", signal],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        return e.stdout if e.stdout else f'Signal "{signal}" not found.'


@mcp.tool
def list_all_modules(path: str) -> str:
    """
    Lists all module definitions in the repository.

    Args:
        path (str): Path to the repository root.

    Returns:
        str: List of module names and their file locations.

    Example:
        >>> list_all_modules("/my/repo")
        'design.sv: module alu(...);\ntb_top.sv: module tb_top(...);\n...'
    """
    try:
        result = subprocess.run(
            [f"cd {path} &&", "git", "grep", "-E", "^module"],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        return e.stdout if e.stdout else 'No modules found.'
    

if __name__ == "__main__":
    print("\n Starting Codebase Search Server...")
    mcp.run(
        transport="sse",
        host="127.0.0.1", 
        port=6969
    )
