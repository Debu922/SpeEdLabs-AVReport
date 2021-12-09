#####################################
#   Author: Debaditya Bhattacharya  #
#   Date:   09 Dec 2021             #
#   e-mail: debbh922@gmail.com      #
#   Desc:   Main file of AV Report  #
#           Generator for SpeEdLabs #
#####################################

def parse_text(path):
    """Opens the text file with lines, parses lines and formats into chunks for TTS engine.

    Returns:
        paragraphs: List of list of lines

    """
    with open(path, "r") as file:
        text = file.readlines()
    paragraph = []
    lines = []
    for line in text:
        if line == "\n":
            paragraph.append(lines)
            lines = []
            continue
        lines.append(line[:-1])
    paragraph.append(lines)
    return paragraph


def merge_lines(text):
    """Merges lines in a paragraph into a single line.

    Args:
        text (List): List of list of lines as generated as paragraphs in parse_text function.

    Returns:
        paragraph (List): Returns list of paragraphs 
    """
    paragraph = []
    for para in text:
        paragraph.append(" ".join(para))
    return paragraph
