from enum import Enum
from htmlnode import *

def text_node_to_html_node(text_node):
    if not isinstance(text_node.text_type, TextType):
        raise TypeError("text_type must be a TextType enum member")
    else:
        match(text_node.text_type):
            case (TextType.TEXT):
                return LeafNode(value = text_node.text)
            
            case (TextType.BOLD):
                return LeafNode("b", text_node.value)
            
            case (TextType.ITALIC):
                return LeafNode("i",text_node.value)
            
            case (TextType.CODE):
                return LeafNode("code",text_node.value)

            case (TextType.LINK):
                return LeafNode("a",text_node.value,{"href": "https://www.google.com"})
            
            case (TextType.IMAGE):
                return LeafNode("img","",{"src":"url/of/image.jpg", "alt":"Description of image"})
# class LeafNode(HTMLNode):
#     def __init__(self, tag = None, value = None, props = None):
#         super().__init__(tag = tag, value = value, children = None, props = props)


class TextType(Enum):
    TEXT = "text"
    BOLD = "**Bold text**"
    ITALIC = "_Italic text_"
    CODE = "`Code text`"
    LINK = "[anchor text](url)"
    IMAGE = "![alt text](url)"

class TextNode:
    def __init__(self,text,text_type,url = None):
        self.text = text
        if not isinstance(text_type, TextType):
            raise TypeError("text_type must be a TextType enum member")
        self.text_type = text_type
        self.url = url

    def __eq__(self,other):
        return self.text == other.text and self.text_type == other.text_type and self.url == other.url
    
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"