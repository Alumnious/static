class HTMLNode:
    def __init__(self, tag = None, value = None, children = None, props = None):
        self.tag = tag
        #string - html tag
        self.value = value
        #string - text to display
        self.children = children
        #list - HTMLNode objects
        self.props = props
        #dictionary - attributes of HTML Tag
    
    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        result = ""
        for prop in self.props.keys():
            result += f' {prop}="{self.props[prop]}"'
        return result
    
    def __repr__(self):
        print(f"Tag = {self.tag}")
        print(f"Value = {self.value}")
        print(f"Children = {self.children}")
        if self.props != None or self.props != {}:
            print(f"Props={self.props}")
        print("")
        return
    
    def __eq__(self, other):
        if not isinstance(other, HTMLNode):
            return False
        return (
            self.tag == other.tag and
            self.value == other.value and
            self.children == other.children and
            self.props == other.props
        )
    
class ParentNode(HTMLNode):
    def __init__(self, tag, children, props = None):
        super().__init__(tag = tag, value = None, children = children, props = props)

    def to_html(self,i = 0):
        if self.tag == None:
            raise ValueError("Needs a tag")
        elif self.children == None:
            raise ValueError("Needs a family. Add children")
        else:
            result = f"<{self.tag}>"
            if self.value != None:
                result += str(self.value)
            
            for child in self.children:
                result += child.to_html(i+1)

            result += f"</{self.tag}>"

            return result
 

class LeafNode(HTMLNode):
    def __init__(self, tag = None, value = None, props = None):
        super().__init__(tag = tag, value = value, children = None, props = props)

    def to_html(self,i = 0):
        if self.value == None:
            raise ValueError("All leaf nodes MUST have a value")
        elif self.tag == None:
            return str(self.value)
        else:
            match(self.tag):
                case ("a"):
                    return f'<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>'
                
                case ("img"):
                    return f'<{self.tag}{self.props_to_html()} />'
                
                case _:
                    return f"<{self.tag}>{self.value}</{self.tag}>"
    
    def __repr__(self):
        print(f"Tag = {self.tag}")
        print(f"Value = {self.value}")
        if self.props != None or self.props != {}:
            print(f"Props = {self.props}")
        print("")
        return
