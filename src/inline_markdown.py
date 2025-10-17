from src.textnode import TextNode, TextType
import re



# Take a list of TextNode objects
# For any node with type TEXT, split its string into a sequence of:
# - plain text nodes
# - image nodes
# - link nodes
# Leave non-TEXT nodes unchanged
# Skip empty text nodes
def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        # Leave non-TEXT nodes unchanged
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        # Grab the original text
        original_text = old_node.text
        # Use the extractor to return any markdown images
        images = extract_markdown_images(original_text)
        # If images returns 0, there are no images, so it's a plain text node.
        # Just append it
        if len(images) == 0:
            new_nodes.append(old_node)
            continue
        # extract_markdown_images returns a list of tuples
        # e.g. [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")]
        for image in images:
            # Split the original text with the image as the delimiter, at most once
            # e.g. This string is before the image ![rick roll](https://i.imgur.com/aKaOqIh.gif) this string is after the image
            sections = original_text.split(f"![{image[0]}]({image[1]})", 1)
            # If 
            if len(sections) != 2:
                raise ValueError("invalid markdown, image section not closed")
            # If there is any text before, emit it as a plain text node
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            # Emit the image node using the alt and url
            new_nodes.append(
                TextNode(
                    image[0],
                    TextType.IMAGE,
                    image[1],
                )
            )
            # Set the original_text to everything after the delimiter
            original_text = sections[1]
        # If there is more original text, emit it as a text node
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))
    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        original_text = old_node.text
        links = extract_markdown_links(original_text)
        if len(links) == 0:
            new_nodes.append(old_node)
            continue
        for link in links:
            sections = original_text.split(f"[{link[0]}]({link[1]})", 1)
            if len(sections) != 2:
                raise ValueError("invalid markdown, link section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))
            original_text = sections[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))
    return new_nodes

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        split_nodes = []
        sections = old_node.text.split(delimiter)
        if len(sections) % 2 == 0:
            raise ValueError("invalid markdown, formatted section not closed")
        for i in range(len(sections)):
            if sections[i] == "":
                continue
            if i % 2 == 0: # 0th and multiples of 2 should be the groupings
                split_nodes.append(TextNode(sections[i], TextType.TEXT)) # This is the text on either side of the delimiter
            else:
                split_nodes.append(TextNode(sections[i], text_type))
        new_nodes.extend(split_nodes)
    return new_nodes

def _assert_all_textnodes(stage, nodes):
    for n in nodes:
        if not isinstance(n, TextNode):
            raise TypeError(f"{stage} produced non-TextNode: {type(n)}: {n}")

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    #_assert_all_textnodes("after CODE", nodes)

    nodes = split_nodes_image(nodes)
    #_assert_all_textnodes("after IMAGE", nodes)

    nodes = split_nodes_link(nodes)
    #_assert_all_textnodes("after LINK", nodes)

    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    #_assert_all_textnodes("after BOLD", nodes)

    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    #_assert_all_textnodes("after ITALIC", nodes)
    return nodes    

# Create a function extract_markdown_images(text) that takes raw markdown text and returns a list of tuples.
# Each tuple should contain the alt text and the URL of any markdown images.
# text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
# print(extract_markdown_images(text))
# # [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")]
def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


# text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
# print(extract_markdown_links(text))
# [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")]
def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


# node = TextNode("This is text with a `code block` word", TextType.TEXT)
# new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
# 
# yields
# 
# [
#     TextNode("This is text with a ", TextType.TEXT),
#     TextNode("code block", TextType.CODE),
#     TextNode(" word", TextType.TEXT),
# ]