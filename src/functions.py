from textnode import *
from htmlnode import *

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    results = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            results.append(node)
            continue
        if node.text.count(delimiter) % 2 != 0:
            raise Exception("Invalid Markdown Syntax: Missing closing delimitter")
        
        split = node.text.split(delimiter)
        if node.text.count(delimiter) > 0:
            results.append(TextNode(split[0], TextType.TEXT))
            results.append(TextNode(split[1], text_type))
            results.append(TextNode(split[2], TextType.TEXT))
    return results

