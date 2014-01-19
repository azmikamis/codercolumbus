import markdown


def apply_markdown(s):
    return markdown.markdown(s, extensions=['codehilite'])
