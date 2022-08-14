import import_data
import json
from pathlib import Path


def main():
    term = "S2022"
    students = import_data.get(term)
    # print(len(students))
    with open(Path('students.json'), 'w') as fileobj:
        json.dump(students, fileobj)


if __name__ == '__main__':
    main()
