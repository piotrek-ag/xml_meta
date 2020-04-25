import re

def remove_leading_spaces(string):
    return re.sub(r"^\s+", "", string)


def remov_trailing_spaces(string):
    return re.sub(r"\s+$", "", string)


def remove_leading_and_trailing_spaces(string):
    return re.sub(r"^\s+|\s+$", "", string)


def remove_all_spaces(string):
    return re.sub(r"\s+", "", string)


def remove_all_commas(string):
    return re.sub(r",", "", string)


def contains_ignore_case(string, pattern):
    pattern = pattern.lower()
    string = string.lower()
    return string.find(pattern) != -1


def split_on_last_dot(prop: str):
    split = prop.split(".")
    return split.pop(len(split)-1)


def equals_ignore_case(first: str, second: str):
    return first.lower() == second.lower()


def trim_new_line_char(string: str):
    if string[-1:] == '\n':
        return string[:-1]
    else:
        return string