import sys
import json
import yaml
import xml.etree.ElementTree as ET


def parse_json(file_path):
    with open(file_path, 'r') as file:
        try:
            data = json.load(file)
            return data
        except json.JSONDecodeError:
            print("Błąd: Nieprawidłowy format pliku JSON.")
            sys.exit(1)


def save_json(file_path, data):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)


def parse_yaml(file_path):
    with open(file_path, 'r') as file:
        try:
            data = yaml.safe_load(file)
            return data
        except yaml.YAMLError:
            print("Błąd: Nieprawidłowy format pliku YAML.")
            sys.exit(1)


def save_yaml(file_path, data):
    with open(file_path, 'w') as file:
        yaml.dump(data, file, default_flow_style=False)


def parse_xml(file_path):
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()
        return root
    except ET.ParseError:
        print("Błąd: Nieprawidłowy format pliku XML.")
        sys.exit(1)


def save_xml(file_path, root):
    tree = ET.ElementTree(root)
    tree.write(file_path, encoding='utf-8', xml_declaration=True)


def convert_file(input_file, output_file):
    if input_file.endswith('.json'):
        data = parse_json(input_file)
        if output_file.endswith('.json'):
            save_json(output_file, data)
        elif output_file.endswith('.yml') or output_file.endswith('.yaml'):
            save_yaml(output_file, data)
        elif output_file.endswith('.xml'):
            print("Błąd: Konwersja z formatu JSON do XML nie jest obsługiwana.")
            sys.exit(1)
        else:
            print("Błąd: Nieobsługiwany format pliku wyjściowego.")
            sys.exit(1)
    elif input_file.endswith('.yml') or input_file.endswith('.yaml'):
        data = parse_yaml(input_file)
        if output_file.endswith('.json'):
            save_json(output_file, data)
        elif output_file.endswith('.yml') or output_file.endswith('.yaml'):
            save_yaml(output_file, data)
        elif output_file.endswith('.xml'):
            print("Błąd: Konwersja z formatu YAML do XML nie jest obsługiwana.")
            sys.exit(1)
        else:
            print("Błąd: Nieobsługiwany format pliku wyjściowego.")
            sys.exit(1)
    elif input_file.endswith('.xml'):
        root = parse_xml(input_file)
        if output_file.endswith('.json'):
            data = xml_to_json(root)
            save_json(output_file, data)
        elif output_file.endswith('.yml') or output_file.endswith('.yaml'):
            print("Błąd: Konwersja z formatu XML do YAML nie jest obsługiwana.")
            sys.exit(1)
        elif output_file.endswith('.xml'):
            save_xml(output_file, root)
        else:
            print("Błąd: Nieobsługiwany format pliku wyjściowego.")
            sys.exit(1)
    else:
        print("Błąd: Nieobsługiwany format pliku wejściowego.")
        sys.exit(1)


def xml_to_json(root):
    data = {}
    if root.attrib:
        data["@attributes"] = root.attrib
    for child in root:
        if child.tag in data:
            if not isinstance(data[child.tag], list):
                data[child.tag] = [data[child.tag]]
            data[child.tag].append(xml_to_json(child))
        else:
            data[child.tag] = xml_to_json(child)
    if root.text:
        text = root.text.strip()
        if data:
            data["#text"] = text
        else:
            data = text
    return data


def main():
    if len(sys.argv) != 3:
        print("Sposób użycia: program.exe pathFile1.x pathFile2.y")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    convert_file(input_file, output_file)


if __name__ == '__main__':
    main()
