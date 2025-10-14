# Block markdown is just the separation of different sections of an entire document
# In well-written markdown, blocks are separated by a single blank line
def markdown_to_blocks(markdown):
    blocks = markdown.split('\n\n')
    new_blocks = []
    for block in blocks:
        b = block.strip()
        if len(b) == 0:
            continue
        new_blocks.append(b)
    return new_blocks