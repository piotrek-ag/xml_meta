from string_tools import *
from flatten import flatten_file

def load_mini_sc():
    return open(INPUT_XML).readlines()


def camel_case_split(str):
    words = [[str[0]]]
    for c in str[1:]:
        if words[-1][-1].islower() and c.isupper():
            words.append(list(c))
        else:
            words[-1].append(c)
    value_ = ''
    for word in words:
        value_ = value_ + ''.join(word) + ' '
        value_ = value_.capitalize()
    return remove_leading_and_trailing_spaces(value_)


def set_type(datatype: str):
    type = datatype.split('@')[1].split('=')[1]
    type = trim_new_line_char(type)
    if equals_ignore_case(type, 'Integer'):
        type = 'Int'
        return type
    if equals_ignore_case(type, 'Boolean'):
        type = 'Bool'
        return type
    if equals_ignore_case(type, "BigDecimal"):
        type = 'BigDec'
        return type
    if equals_ignore_case(type, "String"):
        type = 'Str'
        return type
    else:
        print('Unexpected datatype: ' + type)
        return type


def set_translation_name(category_name: str):
    first_char = category_name[:1]
    first_char = first_char.lower()
    return '_' + first_char + category_name[1:]


# >------------------------------------------------------------------------------------------


PROJECT_ROOT = 'C:\\Users\\piotr.agier\\PycharmProjects\\xml_meta\\'
INPUT_XML = PROJECT_ROOT + 'input.xml'
FLATTENED_XML = PROJECT_ROOT + 'flattened.txt'
OUTPUT = 'output.txt'

file = open(FLATTENED_XML, "w")
file.truncate(0)
flatten_file(INPUT_XML, FLATTENED_XML)

flattened_list = open(FLATTENED_XML, "r").readlines()
flattened_list = [x for x in flattened_list if not contains_ignore_case(x, "@dtype=Default")]

flattened_dtype_list = [x for x in flattened_list if (contains_ignore_case(x, "@dtype") and contains_ignore_case(x, "="))]
flattened_dtype_list = [x[2:] for x in flattened_dtype_list]

flattened_values_list = [x for x in flattened_list if (not contains_ignore_case(x, "@dtype") and contains_ignore_case(x, "="))]
flattened_values_list = [x[2:] for x in flattened_values_list]

category_trans_values: list = []
category_trans_names: list = []

f = open(OUTPUT, "a+")
f.truncate(0)
for prop in flattened_dtype_list:

    # LABEL
    label = "_" + prop.replace('/', '---')
    label = re.sub('@.*', '', label)
    label = label[:-4] + '.label='
    label_value = label.split('---').pop().split('.')[0]
    label_value = camel_case_split(label_value)
    label = label + label_value + '\n'

    # DESCRIPTION
    description = "_" + prop.replace('/', '---')
    description = re.sub('@.*', '', description)
    description = description[:-4] + '.description='
    description = description + label_value + '\n'

    # DATATYPE
    datatype = prop.replace('/', '---')
    path = datatype.split('@')[0][:-3]
    name = '.datatype='
    type = set_type(datatype)
    datatype = path + name + type + '\n'

    # CATEGORY
    category = prop.replace('/', '---')
    category = re.sub('@.*', '', category)
    category_name = category.split('---')[2]
    category_trans_name = set_translation_name(category_name)
    category = category[:-4] + '.category=' + category_trans_name + '\n'

    # add to lists for later use
    category_trans_names.append(category_trans_name)
    category_trans_values.append(camel_case_split(category_name))

    # ORDER
    order = prop.replace('/', '---')
    order = re.sub('@.*', '', order)
    order = order[:-4] + '.order=0' + '\n'

    # TAG 1
    tag_1 = prop.replace('/', '---')
    tag_1 = re.sub('@.*', '', tag_1)
    tag_1 = tag_1[:-4] + '.tag.1=' + category_trans_name + '\n'

    # OUTPUT THE WHOLE RECORD TO FILE
    f.write(label)
    f.write(description)
    f.write(datatype)
    f.write(category)
    f.write(order)
    f.write(tag_1)

    f.write('\n')
    f.write('\n')


# remove duplicates from category lists
category_trans_values = list(dict.fromkeys(category_trans_values))
category_trans_names = list(dict.fromkeys(category_trans_names))


# output_translations
lines: list = []
if range(len(category_trans_names)) == range(len(category_trans_values)):
    lines = category_trans_names
    for i in range(len(lines)):
        lines[i] = lines[i] + '=' + category_trans_values[i]

f.write('\n')
f.write('\n')

for line in lines:
    f.write(line + '\n')