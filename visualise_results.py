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


def draw_classes(sum_points):
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


def main():
    with open(PurePath('./results/sum_points.json'), 'r') as fileobj:
        sum_points = json.load(fileobj)
    draw_classes(sum_points)


if __name__ == '__main__':
    main()
