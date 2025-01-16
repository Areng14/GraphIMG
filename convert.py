import re
import graph

# Sample .graph file content for testing purposes
with open("C:\\Users\\ADMIN\\Dropbox\\My PC (DESKTOP-FBEPBG2)\\Downloads\\GraphIMG\\test.graph","r") as file:
    graph_data = file.read()

# Replace newlines with `;` to treat as separate commands
graph_data = graph_data.replace("\n", ";")

# Valid commands and their associated axes
VALID_CMDS = {
    "LINE": ["x", "y"],
    "INEQUALITY": ["x_less", "x_lesse", "x_great", "x_greate", "y_less", "y_lesse", "y_great", "y_greate"]
}

# Regex to extract commands
cmd_pattern = r"(?P<cmd>LINE|INEQUALITY)\.(?P<axis>\w+)\((?P<expr>.*?)\)\[(?P<range>.*?)\](?: COLOR\((?P<r>\d+), (?P<g>\d+), (?P<b>\d+)\))?"

# Parse each line and validate
for line in graph_data.split(";"):
    line = line.strip()
    if not line:
        continue

    match = re.match(cmd_pattern, line)
    if match:
        cmd = match.group("cmd")
        axis = match.group("axis")
        expr = match.group("expr")
        range_ = match.group("range")
        r = int(match.group("r") or "0")
        g = int(match.group("g") or "0")
        b = int(match.group("b") or "0")

        # Convert color to Matplotlib-compatible format
        color = (int(r) / 255, int(g) / 255, int(b) / 255)

        # Validate the command and axis
        if cmd not in VALID_CMDS:
            print(f"Error: Invalid command '{cmd}' in line: {line}")
            continue
        if axis not in VALID_CMDS[cmd]:
            print(f"Error: Invalid axis '{axis}' for command '{cmd}' in line: {line}")
            continue

        # Process commands
        match cmd:
            case "LINE":
                print(f"Processing LINE: axis={axis}, expr={expr}, range={range_}, color={color}")
                graph.line(axis, expr, range_, (r,g,b))
            case "INEQUALITY":
                inequality_type = axis.split("_")[-1]
                print(f"Processing INEQUALITY: axis={axis}, expr={expr}, range={range_}, color={color}, inequality_type={inequality_type}")
                graph.inequality(axis[:1], expr, range_, (r, g, b), inequality_type)
            case "_":
                print("Didnt implement yet.")
    else:
        print(f"Error: Invalid syntax in line: {line}")

#Export final image
graph.export("C:\\Users\\ADMIN\\Dropbox\\My PC (DESKTOP-FBEPBG2)\\Downloads\\GraphIMG\\image.png")