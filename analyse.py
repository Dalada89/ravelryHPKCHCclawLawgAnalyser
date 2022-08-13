import json
from pathlib import Path


def sum_points(students):
    """
    """
    sum_up = {}
    for student in students:
        print(student['name'])
        if student['house'] not in sum_up.keys():
            sum_up[student['house']] = {
                'classes': {}
            }
        for month in student['classes']:
            if month not in sum_up[student['house']]['classes'].keys():
                sum_up[student['house']]['classes'][month] = {}
            for klasse in student['classes'][month]:
                if klasse not in sum_up[student['house']]['classes'][month].keys():
                    sum_up[student['house']]['classes'][month][klasse] = {
                        'points': 0,
                        'bonus': 0
                    }
                sum_up[student['house']]['classes'][month][klasse]['points'] += student['classes'][month][klasse]['points']
                sum_up[student['house']]['classes'][month][klasse]['bonus'] += student['classes'][month][klasse]['bonus']

    return sum_up


def main():
    """
    """
    with open(Path('./students.json'), 'r') as fileobj:
        students = json.load(fileobj)

    summe = sum_points(students)
    with open(Path('./sum_points.json'), 'w') as fileobj:
        json.dump(summe, fileobj)


if __name__ == '__main__':
    main()
