import pandas as pd
import re
import calendar
import json
from pathlib import Path

students = []


def read_classes(df_sheet, std_points_per_class, part_points_per_class):
    global students
    months = list(calendar.month_name)
    for idx, month in enumerate(months):
        months[idx] = month.lower()
    dict_of_classes = {}
    month_name = ''
    for col in df_sheet.columns:
        possible_class = False
        if re.search('unnamed:', col, re.IGNORECASE):
            possible_class = True
        else:
            month_name = ''
        if col.lower() in months:
            month_name = str(col)
            dict_of_classes[month_name] = {}
            possible_class = True
        # print(df_sheet[col][0])
        # print(type(df_sheet[col][0]))
        if (
            month_name != '' and
            possible_class and
            type(df_sheet[col][0]) != float and
            df_sheet[col][0] != '#' and
            df_sheet[col][0] != ''
        ):
            dict_of_classes[month_name][df_sheet[col][0]] = col

    for idx, row in df_sheet.iterrows():
        # print(row)
        if row['Name'] != '':
            for student in students:
                if row['Name'] == student['name']:
                    student['age'] = str(row['Yr'])
                    if student['age'] in ['nan', 'null']:
                        student['age'] = ''
                    student['classes'] = {}
                    for month_key in dict_of_classes:
                        student['classes'][month_key] = {}
                        for class_key in dict_of_classes[month_key]:
                            student['classes'][month_key][class_key] = {
                                'partial': False,
                                'points': 0,
                                'bonus': 0
                            }
                            points_value = row[dict_of_classes[month_key][class_key]]
                            col_index = df_sheet.columns.get_loc(dict_of_classes[month_key][class_key])
                            # print(str(type(points_value)) + ' ' + str(points_value))
                            if type(points_value) == int:
                                if points_value > 0:
                                    if student['house'] not in ['SOS', 'NQFY']:
                                        partial = False
                                        if str(df_sheet.iloc[idx, col_index+1]).lower() == 'p':
                                            partial = True
                                        if not partial:
                                            student['classes'][month_key][class_key] = {
                                                'partial': False,
                                                'points': std_points_per_class[class_key],
                                                'bonus': points_value - std_points_per_class[class_key]
                                            }
                                        else:
                                            student['classes'][month_key][class_key] = {
                                                'partial': True,
                                                'points': part_points_per_class[class_key],
                                                'bonus': points_value - part_points_per_class[class_key]
                                            }
                                    else:
                                        student['classes'][month_key][class_key] = {
                                                'partial': True,
                                                'points': 0,
                                                'bonus': 0,
                                                'took_part': True
                                            }

                    # print(student['name'])
    # print(dict_of_classes)

    return None


def read_quidditch(df_sheet):
    global students

    matches = ['Match 1', 'Match 2', 'Match 3', 'Match 4']
    match_name = ''
    dict_of_matches = {}

    for col in df_sheet.columns:
        possible_class = False
        if re.search('unnamed:', col, re.IGNORECASE):
            possible_class = True
        else:
            match_name = ''

        if col in matches:
            match_name = str(col)
            dict_of_matches[match_name] = {}
            possible_class = True
        # print(df_sheet[col][0])
        # print(type(df_sheet[col][0]))
        if (
            match_name != '' and
            possible_class and
            type(df_sheet[col][0]) != float and
            df_sheet[col][0] != '#' and
            df_sheet[col][0] != ''
        ):
            dict_of_matches[match_name][df_sheet[col][0]] = col

    for idx, row in df_sheet.iterrows():
        # print(row)
        if row['Student'] != '':
            for student in students:
                if str(row['Student']) == 'nan':
                    continue
                if row['Student'].lower() == student['name'].lower():
                    student['quidditch'] = {}
                    for match in dict_of_matches:
                        student['quidditch'][match] = {
                            'base': 0,
                            'bonus': 0,
                            'post': 0
                        }
                        student['quidditch'][match] = {}
                        base_col = dict_of_matches[match]['base']
                        bonus_col = dict_of_matches[match]['bp']
                        if type(row[base_col]) == int:
                            if row[base_col] > 0:
                                student['quidditch'][match]['base'] = row[base_col]
                                bonus = row[bonus_col]
                                if str(bonus) == 'nan':
                                    student['quidditch'][match]['bonus'] = 0
                                else:
                                    student['quidditch'][match]['bonus'] = bonus
                                student['quidditch'][match]['post'] = row[match]

    return None


def read_dragons():
    return None


def read_owls():
    return None


def read_newt():
    return None


def read_hmc():
    return None


def read_ootp():
    return None


def read_students(df_sheet):
    global students
    not_relevant_pattern = r'[shrgn]{1}[\d]{2,3}'

    for index, row in df_sheet.iterrows():
        match = re.fullmatch(not_relevant_pattern, row['Name'], re.IGNORECASE)

        if match is None:
            match = re.fullmatch(r'sos[\d]{2,3}', row['Name'], re.IGNORECASE)

        if match is None:
            students.append({
                'name': row['Name'],
                'house': str(row['House']).replace('-', ''),
                'age': None
            })

    return None


def load_sheets(xlsxpath):
    list_of_sheets = [
        'Dorms',
        'Classes +',
        'vLookup',
        'Quidditch'
    ]
    df_sheets = pd.read_excel(xlsxpath, sheet_name=list_of_sheets)
    return df_sheets


def get(term):
    global students
    configfile = Path('./data/config_{term}.json'.format(term=term))
    with open(configfile, 'r') as fileobj:
        config = json.load(fileobj)
    xlsxpath = Path(config['file'])
    df_sheets = load_sheets(xlsxpath)

    # read_classes(df_sheets['Classes +'])

    read_students(df_sheets['vLookup'])
    read_quidditch(df_sheets['Quidditch'])
    read_classes(df_sheets['Classes +'], config['std_points_per_class'], config['part_points_per_class'])

    return students


if __name__ == '__main__':
    get()
