class HTMLNode():
    def __init__(self, tag = None, value = None, children = None, props = None):
        self.tag = tag
        self.value = value
        self.children = children # A list of HTMLNode objects representing the children of this node
        self.props = props
   
    def to_html(self):
        raise NotImplementedError("Child classes will override this method to render themselves as HTML")

    def props_to_html(self):
        ret_str = ""
        if not self.props:
            return ""
        parts = []
        # Iterate over a asc sorted list to get deterministic results
        for k, v in sorted(self.props.items()):
            parts.append(f' {k}="{v}"')
        return "".join(parts)

    def __repr__(self):
        return (f"HTMLNode(tag={self.tag!r}, value={self.value!r}, children={self.children!r}, props={self.props!r})")
