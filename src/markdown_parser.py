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
            temp += "\n" + line
        else:
            temp = line
    if len(temp) > 0:
        blocks.append(temp)
    return blocks

def extract_title(markdown):
    matches = re.findall(r"(^# )(.*)", markdown, re.MULTILINE)
    if len(matches) > 0 and len(matches[0]) == 2:
        return matches[0][1]
    else:
        raise Exception("No title found")

def block_to_block_type(block):
    type, _ = parse_block(block)
    return type

def parse_block(block):
    matches = re.findall(r"(^#{1,6} )(.*)", block)
    if len(matches) == 1 and len(matches[0]) == 2:
        # Return the heading part as well so we can tell later what level of heading to apply
        values = [ matches[0][0].strip(), matches[0][1] ]
        return (BlockType.HEADING, values)
    
    matches = re.findall(r"(^`{3})([\s\S]*)(`{3}$)", block)
    if len(matches) == 1 and len(matches[0]) == 3:
        code = matches[0][1].strip("\n")
        return (BlockType.CODE, [ code ])
    
    lines = block.strip().split("\n")
    block_types = {}
    li_num = 1
    for line in lines:
        if len(line) < 1:
            continue

        matches = re.findall(r"(^> ?)(.*)", line)
        if len(matches) == 1 and len(matches[0]) == 2:
            if BlockType.QUOTE not in block_types:
                block_types[BlockType.QUOTE] = []
            block_types[BlockType.QUOTE].append(matches[0][1])
            continue

        matches = re.findall(r"(^[\*-] )(.*)", line)
        if len(matches) == 1 and len(matches[0]) == 2:
            if BlockType.UNORDERED_LIST not in block_types:
                block_types[BlockType.UNORDERED_LIST] = []
            block_types[BlockType.UNORDERED_LIST].append(matches[0][1])
            continue

        matches = re.findall(r"(^\d+\. )(.*)", line)
        if len(matches) == 1 and len(matches[0]) == 2:
            li_str = str(li_num)
            if line[:len(li_str)] == li_str:
                if BlockType.ORDERED_LIST not in block_types:
                    block_types[BlockType.ORDERED_LIST] = []
                block_types[BlockType.ORDERED_LIST].append(matches[0][1])
                li_num += 1
                continue
        
        if BlockType.PARAGRAPH not in block_types:
            block_types[BlockType.PARAGRAPH] = []
        block_types[BlockType.PARAGRAPH].append(line)

    if len(block_types) == 1:
        type, values = list(block_types.items())[0]
        return (type, values)
    combined_list = [item for sublist in block_types.values() for item in sublist]
    return (BlockType.PARAGRAPH, combined_list)
