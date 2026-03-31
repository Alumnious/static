from textnode import *
from htmlnode import *
from enum import Enum
import re
from os.path import exists, join, isfile
import os
from os import mkdir, listdir
from shutil import copy, rmtree
import pathlib

class BlockType(Enum):
    PARAGRAPH = "text"
    HEADING = "**Bold text**"
    CODE = "_Italic text_"
    QUOTE = "`Code text`"
    UNORDERED_LIST = "[anchor text](url)"
    ORDERED_LIST = "![alt text](url)"

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    results = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            results.append(node)
            continue
            
        parts = node.text.split(delimiter)
        if len(parts) % 2 == 0:
            raise Exception(f"Invalid Markdown: No closing '{delimiter}' found in text: '{node.text}'")
        
        for i in range(len(parts)):
            # Don't 'continue' here! Just check if empty before appending.
            if i % 2 == 0:
                if parts[i] != "":
                    results.append(TextNode(parts[i], TextType.TEXT))
            else:
                if parts[i] != "":
                    results.append(TextNode(parts[i], text_type))
    return results

def extract_markdown_image(text: str):
    matches = re.findall(r"!\[(.*?)\]\((.*?)\)", text)
    return matches

def extract_markdown_link(text: str):
    matches = re.findall(r"(?<!\!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        
        images = extract_markdown_image(node.text)
        if not images:
            new_nodes.append(node)
            continue

        current_text = node.text
        for alt, url in images:
            sections = current_text.split(f"![{alt}]({url})", 1)
            if sections[0]:
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(alt, TextType.IMAGE, url))
            current_text = sections[1]
        
        if current_text:
            new_nodes.append(TextNode(current_text, TextType.TEXT))
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        
        links = extract_markdown_link(node.text)
        if not links:
            new_nodes.append(node)
            continue

        current_text = node.text
        for alt, url in links:
            sections = current_text.split(f"[{alt}]({url})", 1)
            if sections[0]:
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(alt, TextType.LINK, url))
            current_text = sections[1]
        
        if current_text:
            new_nodes.append(TextNode(current_text, TextType.TEXT))
    return new_nodes

def text_to_textnodes(text):
        nodes = [TextNode(text, TextType.TEXT)]

        nodes = split_nodes_image(nodes)
        nodes = split_nodes_link(nodes)
        nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
        nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
        return nodes

def markdown_to_blocks(markdown):
    results = []
    split = markdown.split("\n\n")
    for block in split:
        results.append(block.strip())
    return results

def block_to_block_type(block):

    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING

    if block.startswith("```") and block.endswith("```") and len(block) != 3:
        return BlockType.CODE
    
    lines: list[str] = block.split("\n")
    every_line_char_start = True
    for line in lines:
        if line.startswith(">") != True:
            every_line_char_start = False
            break
    if every_line_char_start == True:
        return BlockType.QUOTE
    
    every_line_char_start = True
    for line in lines:
        if line.startswith("* ") != True and line.startswith("- ") != True:
            every_line_char_start = False
            break
    if every_line_char_start == True:
        return BlockType.UNORDERED_LIST
    
    num = 1
    every_line_char_start = True
    for line in lines:
        if line.startswith(f"{num}.") != True:
            every_line_char_start = False
            break
        num += 1
    if every_line_char_start == True:
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH

def quote_block_to_html_node(block: str) -> HTMLNode:
    lines: str = block.splitlines()
    lines = list(map(lambda line: line.lstrip("> "), lines))
    cleaned_block = "<br>".join(lines)
    text_nodes: list[TextNode] = text_to_textnodes(cleaned_block)
    html_nodes: list[HTMLNode] = list(map(text_node_to_html_node, text_nodes))
    quote_html_node: ParentNode = ParentNode(tag="blockquote", children=html_nodes, props=None)
    return quote_html_node

def unordered_list_block_to_html_node(block: str) -> HTMLNode:
    lines: str = block.splitlines()
    lines = list(map(lambda line: line[2:], lines))
    list_items: list[HTMLNode] = []
    for line in lines:
        text_nodes: list[TextNode] = text_to_textnodes(line)
        html_nodes: list[HTMLNode] = list(map(text_node_to_html_node, text_nodes))
        list_item: ParentNode = ParentNode(tag="li", children=html_nodes, props=None)
        list_items.append(list_item)
    unordered_list: ParentNode = ParentNode(tag="ul", children=list_items, props=None)
    return unordered_list

def ordered_list_block_to_html_node(block: str) -> HTMLNode:
    lines: str = block.splitlines()
    lines = list(map(lambda line: line[line.find(".") + 2:], lines))
    list_items: list[HTMLNode] = []
    for line in lines:
        text_nodes: list[TextNode] = text_to_textnodes(line)
        html_nodes: list[HTMLNode] = list(map(text_node_to_html_node, text_nodes))
        list_item: ParentNode = ParentNode(tag="li", children=html_nodes, props=None)
        list_items.append(list_item)
    ordered_list: ParentNode = ParentNode(tag="ol", children=list_items, props=None)
    return ordered_list

def code_block_to_html_node(block: str) -> HTMLNode:
    lines: str = block.splitlines()
    if lines[0] == "```\n" or lines[0] == "```":
        lines = lines[1:]
    if lines[len(lines) - 1] == "```":
        lines = lines[:-1]
    lines = list(map(lambda line: line.lstrip("`"), lines))
    lines = list(map(lambda line: line.rstrip("`"), lines))
    cleaned_block = "<br>".join(lines)
    text_nodes: list[TextNode] = text_to_textnodes(cleaned_block)
    html_nodes: list[HTMLNode] = list(map(text_node_to_html_node, text_nodes))
    code_html_node: ParentNode = ParentNode(tag="code", children=html_nodes, props=None)
    pre_html_node: ParentNode = ParentNode(tag="pre", children=[code_html_node], props=None)
    return pre_html_node

def heading_block_to_html_node(block: str) -> HTMLNode:
    heading: str = ""
    if block.startswith("######"):
        heading = "h6"
    elif block.startswith("#####"):
        heading = "h5"
    elif block.startswith("####"):
        heading = "h4"
    elif block.startswith("###"):
        heading = "h3"
    elif block.startswith("##"):
        heading = "h2"
    elif block.startswith("#"):
        heading = "h1"
    line: str = block.lstrip("# ")
    text_nodes: list[TextNode] = text_to_textnodes(line)
    html_nodes: list[HTMLNode] = list(map(text_node_to_html_node, text_nodes))
    heading_html_node: ParentNode = ParentNode(tag=heading, children=html_nodes, props=None)
    return heading_html_node

def paragraph_block_to_html_node(block: str) -> HTMLNode:
    text_nodes: list[TextNode] = text_to_textnodes(block)
    html_nodes: list[HTMLNode] = list(map(text_node_to_html_node, text_nodes))
    paragraph_html_node: ParentNode = ParentNode(tag="p", children=html_nodes, props=None)
    return paragraph_html_node

def markdown_to_html_node(markdown: str) -> HTMLNode:
    blocks: list[str] = markdown_to_blocks(markdown)
    block_html_nodes: list[HTMLNode] = []
    for block in blocks:
        block_type: str = block_to_block_type(block)
        if block_type == BlockType.QUOTE:
            block_html_nodes.append(quote_block_to_html_node(block))
        elif block_type == BlockType.UNORDERED_LIST:
            block_html_nodes.append(unordered_list_block_to_html_node(block))
        elif block_type == BlockType.ORDERED_LIST:
            block_html_nodes.append(ordered_list_block_to_html_node(block))
        elif block_type == BlockType.CODE:
            block_html_nodes.append(code_block_to_html_node(block))
        elif block_type == BlockType.HEADING:
            block_html_nodes.append(heading_block_to_html_node(block))
        else:
            block_html_nodes.append(paragraph_block_to_html_node(block))
    root: HTMLNode = ParentNode(tag="div", children=block_html_nodes, props=None)
    return root

def copy_dir(src: str, dest: str):
    if not exists(dest):
        mkdir(dest)
        print(f"{dest} is created")

    dir_list: list[str] = listdir(src)
    print(dir_list)
    for dir in dir_list:
        if isfile(join(src, dir)):
            print(f" * {join(src, dir)} -> {join(dest, dir)}")
            copy(join(src, dir), join(dest, dir))
        else:
            copy_dir(src=join(src, dir), dest=join(dest, dir))

def copy_static():
    if exists("public"):
        print("Removing old public dir")
        rmtree("public")

    print("Creating new public dir")
    mkdir("public")
    copy_dir(src="static", dest="public")

def extract_title(markdown: str) -> str:
    if markdown.startswith("# "):
        title: str = markdown.split("\n", 1)[0]
        title = markdown.lstrip("# ")
        return title
    else:
        raise Exception("No title present")
    
def generate_page(from_path: str, template_path: str, dest_path: str):
    print(f"Building page from: {from_path} to: {dest_path} using: {template_path}")
    markdown_file = open(from_path)
    markdown: str = markdown_file.read()
    markdown_file.close()
    template_file = open(template_path)
    template: str = template_file.read()
    template_file.close()
    markdown_html: str = markdown_to_html_node(markdown).to_html()
    title: str = extract_title(markdown)
    page: str = template.replace("{{ Title }}", title).replace("{{ Content }}", markdown_html)
    if not os.path.exists(os.path.dirname(dest_path)):
        os.makedirs(os.path.dirname(dest_path))
    dest_file = open(dest_path, "w")
    dest_file.write(page)
    dest_file.close()

def generate_page_recursive(dir_path_content: str, template_path: str, dest_dir_path: str):
    for dir in os.listdir(dir_path_content):
        if os.path.isfile(os.path.join(dir_path_content, dir)):
            if pathlib.PurePath(dir).suffix == ".md":
                generate_page(os.path.join(dir_path_content, dir), template_path, os.path.join(dest_dir_path, f"{pathlib.PurePath(dir).stem}.html"))
        else:
            generate_page_recursive(os.path.join(dir_path_content, dir), template_path, os.path.join(dest_dir_path, dir))