import xml.etree.ElementTree as ET


def removeNS(tag):
    if tag.find('}') == -1:
        return tag
    else:
        return tag.split('}', 1)[1]


def linearize(el, path, path_to_flattened_xml):
    # Print text value if not empty
    text = el.text.strip()
    if text == "":
        # print(path)
        f = open(path_to_flattened_xml, "a+")
        f.write(path + '\n')
    else:

        # Several lines ?
        lines = text.splitlines()
        if len(lines) > 1:
            lineNb = 1
            for line in lines:
                # print(path + "[line %d]=%s " % (lineNb, line))
                f = open(path_to_flattened_xml, "a+")
                f.write(path + "[line %d]=%s " % (lineNb, line) + '\n')
                lineNb += 1
        else:
            # print(path + "=" + text)
            f = open(path_to_flattened_xml, "a+")
            f.write(path + "=" + text + '\n')

    # Print attributes
    for name, val in el.items():
        # print(path + "/@" + removeNS(name) + "=" + val)
        f = open(path_to_flattened_xml, "a+")
        f.write(path + "/@" + removeNS(name) + "=" + val + '\n')

    # Counter on the sibbling element names
    counters = {}

    # Loop on child elements
    for childEl in el:

        # Remove namespace
        tag = removeNS(childEl.tag)

        # Tag name already encountered ?
        if tag in counters:
            counters[tag] += 1
            # Number it
            numberedTag = tag + "[" + str(counters[tag]) + "]"
        else:
            counters[tag] = 1
            numberedTag = tag

        # Print child node recursively
        linearize(childEl, path + '/' + numberedTag, path_to_flattened_xml)


# Main
def process(stream, prefix, path_to_flattened_xml):
    # Parse the XML
    tree = ET.parse(stream)

    # Get root element
    root = tree.getroot()

    # Linearize
    linearize(root, prefix + "//" + removeNS(root.tag), path_to_flattened_xml)


# >---------------------------------------------------------------------


def flatten_file(filename, path_to_flattened_xml):
    file = open(filename)
    prefix = ""
    process(file, prefix, path_to_flattened_xml)