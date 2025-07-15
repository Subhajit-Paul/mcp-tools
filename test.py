from fastmcp import FastMCP

mcp = FastMCP(name="TestServer")

@mcp.tool
def mul(a: int, b: int) -> int:
    """Takes two integers as inputs and provides multiplication result

    Args:
        a (int): Number 1
        b (int): Number 2

    Returns:
        int: Result
    """
    return a*b


if __name__ == "__main__":
    print("\n Starting Test Server...")
    mcp.run(
        transport="sse",
        host="127.0.0.1", 
        port=6969
    )
