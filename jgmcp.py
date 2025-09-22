from fastmcp import FastMCP
import subprocess
mcp = FastMCP(name="JasperGoldMCPServer")

@mcp.tool
def write_assertion_to_file(assertion: str):
    """
    Writes the provided assertion string to a file named 'assertion.sv'.

    Args:
        assertion (str): The assertion string to be written to the file.

    Returns:
        str: A message indicating the success of the operation.
    """
    try:
        with open("/home/src2024/mcp-demo/default/assert.sv", "r") as f:
            content = f.read()
        with open("assertion.sv", "w") as f:
            f.write(content.replace("endmodule", f"{assertion}\nendmodule"))
        return "Assertion written to assertion.sv"
    except Exception as e:
        return f"Error writing assertion to file: {e}"
    
@mcp.tool
def run_jaspergold():
    """
    Executes the JasperGold tool with a predefined script.

    Returns:
        str: The output from the JasperGold command or an error message if it fails.
    """
    try:
        _ = subprocess.run(
            ["jg", "default.tcl"],
            cwd="/home/src2024/mcp-demo",
            capture_output=True,
            text=True,
            check=True
        )
        return "JasperGold ran successfully"
    except subprocess.CalledProcessError as e:
        return f"Error running JasperGold: {e.stderr}"

@mcp.tool
def read_jaspergold_report():
    """
    Reads the JasperGold report file and returns its content.

    Returns:
        str: The content of the JasperGold report or an error message if it fails.
    """
    try:
        with open("/home/src2024/mcp-demo/report.txt", "r") as f:
            report = f.read()
        return report
    except Exception as e:
        return f"Error reading JasperGold report: {e}"