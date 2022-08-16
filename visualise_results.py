"""
This file should visualise the imported and analysed data
"""
import json
from pathlib import PurePath
import matplotlib.pyplot as plt


houses = {
    'Ravenclaw': '#271bff',
    'Hufflepuff': '#e0e13e',
    'Slytherin': '#00ba33',
    'Gryffindor': '#d30004'
}


def draw_classes(sum_points, students):
    list_of_classes = list(sum_points['Ravenclaw']['classes']['MAY'].keys())
    # classes = []
    months = ['MAY', 'JUNE', 'JULY']
    term = 'S2022'
    for klasse in list_of_classes:
        fig, ax = plt.subplots()
        for house in houses:
            line_points = []
            line_bonus = []
            for month in months:
                line_points.append(sum_points[house]['classes'][month][klasse]['points'])
                line_bonus.append(sum_points[house]['classes'][month][klasse]['points'] +
                                  sum_points[house]['classes'][month][klasse]['bonus'])

            ax.plot(months, line_points, linestyle='dotted', color=houses[house])
            ax.plot(months, line_bonus, linestyle='solid', color=houses[house], label=house)
        ax.grid()
        ax.legend()
        ax.set_ylabel('Overall and bonus points')
        ax.set_title(klasse + ' ' + term)
        save_name = './results/plots/{term}_cls_{klasse}.png'
        plt.savefig(PurePath(save_name.format(term=term, klasse=klasse)), dpi=300)

    for klasse in list_of_classes:
        bx_data = {}
        for month in months:
            bx_data[month] = {}
            for house in houses:
                bx_data[month][house] = []
        for student in students:
            if 'classes' not in student:
                continue
            for month in months:
                points = student['classes'][month][klasse]['points'] + student['classes'][month][klasse]['bonus']
                if points > 0:
                    bx_data[month][student['house']].append(points)
        for month in months:
            fig, ax = plt.subplots()
            colums = []
            for house in houses:
                colums.append(bx_data[month][house])
            box = ax.boxplot(colums, notch=True, patch_artist=True)
            for patch, house in zip(box['boxes'], houses):
                patch.set_facecolor(houses[house])
            ax.set_xticks([1, 2, 3, 4], houses, rotation=0)
            ax.grid(axis='y')
            ax.set_ylabel('Points per student')
            ax.set_title(klasse + ' ' + term + ' ' + month)
            save_name = './results/plots/{term}_bx_cls_{klasse}_{m}.png'
            plt.savefig(PurePath(save_name.format(term=term, klasse=klasse, m=month)), dpi=300)


def main():
    with open(PurePath('./results/students.json'), 'r') as fileobj:
        students = json.load(fileobj)
    with open(PurePath('./results/sum_points.json'), 'r') as fileobj:
        sum_points = json.load(fileobj)
    draw_classes(sum_points, students)


if __name__ == '__main__':
    main()
