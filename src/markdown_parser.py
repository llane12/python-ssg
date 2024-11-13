def markdown_to_blocks(markdown):
    lines = markdown.split("\n")
    
    blocks = []
    temp = ""
    for line in lines:
        stripped = line.strip()
        if len(stripped) == 0 and len(temp) > 0:
            blocks.append(temp)
            temp = ""
        elif len(temp) > 0:
            temp += "\n" + stripped
        else:
            temp = stripped
    if len(temp) > 0:
        blocks.append(temp)
    return blocks
