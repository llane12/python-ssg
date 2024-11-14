from enum import Enum
import re


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


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

def block_to_block_type(block):
    matches = re.findall(r"(^#{1,6} )(.*)", block)
    if len(matches) == 1 and len(matches[0]) == 2:
        return BlockType.HEADING
    matches = re.findall(r"(^`{3})([\s\S]*)(`{3}$)", block)
    if len(matches) == 1 and len(matches[0]) == 3:
        return BlockType.CODE
    
    lines = block.split("\n")
    block_types = set()
    li_num = 1
    for line in lines:
        if len(line) < 1:
            continue
        if line[0] == ">":
            block_types.add(BlockType.QUOTE)
            continue

        matches = re.findall(r"(^[\*-] )(.*)", line)
        if len(matches) == 1 and len(matches[0]) == 2:
            block_types.add(BlockType.UNORDERED_LIST)
            continue

        matches = re.findall(r"(^\d+\. )(.*)", line)
        if len(matches) == 1 and len(matches[0]) == 2:
            li_str = str(li_num)
            if line[:len(li_str)] == li_str:
                block_types.add(BlockType.ORDERED_LIST)
                li_num += 1
                continue
        
        block_types.add(BlockType.PARAGRAPH)
    if len(block_types) == 1:
        return block_types.pop()
    else:
        return BlockType.PARAGRAPH
