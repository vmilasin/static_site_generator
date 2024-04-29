from block_markdown import markdown_to_blocks



def main():
    md = """
This is **bolded** paragraph




This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line

* This is a list
* with items
"""

    blocks = markdown_to_blocks(md)
    for block in blocks:
        print(block)



main()