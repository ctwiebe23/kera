"""
AUTHOR  : Carston Wiebe
DATE    : AUG 18 2025
SHORT   : Populate templates with data
USAGE   : malline PLATE_FILES... DATA_FILES...
EXAMPLE : malline select.sql.plate procedure.sql.plate table1.json table2.yml table3.yaml
"""

from enum import Flag, auto
from pathlib import Path
import yaml
import json
import sys

OUT_FILE_KEY = "_out_file"
OUT_DIR_OPT = ["-o", "--out"]

class Position(Flag):
    IDLE = auto()
    ESCAPED = auto()
    HASH = auto()
    SLOT = auto()
    KEY = auto()
    END_HASH = auto()
    CONDITION_KEY_START = auto()
    CONDITION_KEY = auto()
    CONDITION_KEY_CLOSE = auto()
    CONDITION_KEY_AFTER = auto()
    CONDITION_BODY_START = auto()
    CONDITION_BODY = auto()
    CONDITION_BODY_AFTER = auto()
    CONDITION_FALLBACK_START = auto()
    CONDITION_FALLBACK = auto()
    COLLECTION_BODY_START = auto()
    COLLECTION_BODY = auto()
    COLLECTION_JOIN = auto()
    COLLECTION_JOIN_AFTER = auto()

VALID_KEY_CHARS = "QWERTYUIOPASDFGHJKLZXCVBNMqwertyuiopasdfghjklzxcvbnm1234567890-_"
WHITESPACE_CHARS = " \t\n"

def resolve_key(data, key):
    if key in data:
        return data[key]
    else:
        return ""

def trim_body(body):
    start_index = 0
    end_index = len(body) - 1

    def safe():
        return start_index < len(body) and end_index > -1

    while safe() and body[start_index] == " ":
        start_index += 1

    if safe() and body[start_index] == "\n":
        start_index += 1

    while safe() and body[end_index] == " ":
        end_index -= 1

    if safe() and body[end_index] == "\n":
        end_index -= 1

    return body[start_index:end_index+1]

def get_body_end(plate, start_index):
    num_open = 0
    i = start_index
 
    while i < len(plate):
        if i == len(plate) - 1:
            return -1

        if plate[i:i+2] == "}}":
            if num_open == 0:
                return i
            else:
                num_open -= 1
                i += 1
        elif plate[i:i+2] == "{{":
            num_open += 1
            i += 1

        i += 1

def process(plate, data):
    i = 0
    buffer = ""
    key = ""
    join_str = "\n"
    condition_status = True
    current_position = Position.IDLE

    def reprocess():
        nonlocal i, current_position
        i -= 1
        current_position = Position.IDLE

    while i < len(plate):
        char = plate[i]

        match current_position:
            case Position.IDLE:
                if char == "#":
                    current_position = Position.HASH
                elif char == "\\":
                    current_position = Position.ESCAPED
                else:
                    buffer += char

            case Position.ESCAPED:
                if char != "#":
                    buffer += "\\"
                buffer += char
                current_position = Position.IDLE

            case Position.HASH:
                if char == "#":
                    current_position = Position.SLOT
                else:
                    buffer += "#"
                    reprocess()

            case Position.SLOT:
                if char == "[":
                    current_position = Position.CONDITION_KEY_START
                elif char in VALID_KEY_CHARS:
                    current_position = Position.KEY
                    key = char
                else:
                    buffer += "##"
                    reprocess()

            case Position.CONDITION_KEY_START:
                if char in WHITESPACE_CHARS:
                    pass
                if char in VALID_KEY_CHARS:
                    current_position = Position.CONDITION_KEY
                    key = char
                else:
                    print(f"expected key, found {char}")
                    reprocess()

            case Position.CONDITION_KEY_CLOSE:
                if char in WHITESPACE_CHARS:
                    pass
                if char == "]":
                    value = resolve_key(data, key)
                    current_position = Position.CONDITION_KEY_AFTER
                    condition_status = True if value else False
                else:
                    print(f"expected '[' found {char}")
                    reprocess()

            case Position.CONDITION_KEY_AFTER:
                if char == "{":
                    current_position = Position.CONDITION_BODY_START
                else:
                    print(f"expected '{{' found {char}")
                    reprocess()

            case Position.KEY:
                if char in VALID_KEY_CHARS:
                    key += char
                elif char == "{":
                    current_position = Position.COLLECTION_BODY_START
                elif char == "(":
                    current_position = Position.COLLECTION_JOIN
                    join_str = ""
                elif char == "#":
                    current_position = Position.END_HASH
                else:
                    buffer += "##" + key
                    reprocess()

            case Position.END_HASH:
                if char == "#":
                    buffer += str(resolve_key(data, key))
                    current_position = Position.IDLE
                else:
                    buffer += "##" + key + "#"
                    reprocess()

            case Position.CONDITION_KEY:
                if char in VALID_KEY_CHARS:
                    key += char
                elif char in WHITESPACE_CHARS:
                    current_position = Position.CONDITION_KEY_CLOSE
                elif char == "]":
                    value = resolve_key(data, key)
                    current_position = Position.CONDITION_KEY_AFTER
                    condition_status = True if value else False
                else:
                    print(f"expected ']' found {char}")
                    reprocess()

            case Position.CONDITION_BODY_START:
                if char == "{":
                    current_position = Position.CONDITION_BODY
                else:
                    print(f"expected '{{' found {char}")
                    reprocess()

            case Position.COLLECTION_BODY_START:
                if char == "{":
                    current_position = Position.COLLECTION_BODY
                else:
                    print(f"expected '{{' found {char}")
                    reprocess()

            case Position.CONDITION_BODY:
                end_index = get_body_end(plate, i)
                if end_index == -1:
                    print("bad condition body: " + plate[i:])
                    reprocess()
                else:
                    if condition_status:
                        body = trim_body(plate[i:end_index])
                        buffer += process(body, data)
                    current_position = Position.CONDITION_BODY_AFTER
                    i = end_index + 1

            case Position.CONDITION_BODY_AFTER:
                if char == "{":
                    current_position = Position.CONDITION_FALLBACK_START
                else:
                    reprocess()

            case Position.CONDITION_FALLBACK_START:
                if char == "{":
                    current_position = Position.CONDITION_FALLBACK
                else:
                    buffer += "{"
                    reprocess()

            case Position.CONDITION_FALLBACK:
                end_index = get_body_end(plate, i)
                if end_index == -1:
                    print("bad fallback body: " + plate[i:])
                    reprocess()
                else:
                    if not condition_status:
                        body = trim_body(plate[i:end_index])
                        buffer += process(body, data)
                    current_position = Position.CONDITION_BODY_AFTER
                    i = end_index + 1

            case Position.COLLECTION_BODY:
                end_index = get_body_end(plate, i)
                if end_index == -1:
                    print("bad collection body: " + plate[i:])
                    reprocess()
                else:
                    body = trim_body(plate[i:end_index])
                    sub_process = lambda d: process(body, d)
                    sub_datas = resolve_key(data, key)
                    if hasattr(sub_datas, "__iter__"):
                        results = map(sub_process, sub_datas)
                        results = filter(lambda r: r, results)
                        buffer += join_str.join(results)
                    else:
                        print(f"expected key with type 'list' found {type(sub_datas)}")
                    join_str = "\n"
                    current_position = Position.IDLE
                    i = end_index + 1

            case Position.COLLECTION_JOIN:
                if char == ")":
                    current_position = Position.COLLECTION_JOIN_AFTER
                elif char == "\\":
                    i += 1
                    if i < len(plate):
                        escaped_char = plate[i]
                        join_str += "\n" if escaped_char == "n" else escaped_char
                else:
                    join_str += char

            case Position.COLLECTION_JOIN_AFTER:
                if char == "{":
                    current_position = Position.COLLECTION_BODY_START
                else:
                    print(f"expected '{{' found {char}")
                    reprocess()

            case _:
                print(f"bad position: {current_position}")
                reprocess()

        i += 1

    return buffer

def main():
    plates = []
    datas = []

    out_dir = Path(".")
    expecting_out_dir = False

    for arg in sys.argv[1:]:
        if expecting_out_dir:
            out_dir = Path(arg)
            if not out_dir.is_dir():
                out_dir.mkdir()
            expecting_out_dir = False
            continue

        if arg in OUT_DIR_OPT:
            expecting_out_dir = True
            continue

        file = Path(arg)
        if not file.is_file():
            print(f"{file} is not a file")
            continue

        name = file.stem

        if file.match("*.json"):
            data = file.read_text()
            data = json.loads(data)
            datas.append((data, name))
        elif file.match("*.yaml") or file.match("*.yml"):
            data = file.read_text()
            data = yaml.safe_load(data)
            datas.append((data, name))
        else:
            if not file.match("*.plate"):
                name = file.name
            plate = file.read_text()
            plates.append((plate, name))
    
    for plate, plate_name in plates:
        for data, data_name in datas:
            if OUT_FILE_KEY in data:
                name = data[OUT_FILE_KEY]
            else:
                name = data_name + "_" + plate_name
            result = process(plate, data)
            (out_dir / Path(name)).write_text(result)
    
if __name__ == "__main__":
    main()
