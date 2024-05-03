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
    
    ov_tmp_points = {}
    ov_tmp_bonus = {}
    for house in houses:
        ov_tmp_points[house] = 0
        ov_tmp_bonus[house] = 0
    for klasse in list_of_classes:
        fig, ax = plt.subplots()
        dist_points = []
        dist_bonus = []
        dist_points_perc = []
        dist_bonus_perc = []
        for house in houses:
            line_points = []
            line_bonus = []
            line_overall = []
            tmp_points = 0
            tmp_bonus = 0
            for month in months:
                tmp_points += sum_points[house]['classes'][month][klasse]['points']
                tmp_bonus += sum_points[house]['classes'][month][klasse]['bonus']
                line_points.append(sum_points[house]['classes'][month][klasse]['points'])
                line_bonus.append(sum_points[house]['classes'][month][klasse]['bonus'])
                line_overall.append(sum_points[house]['classes'][month][klasse]['points'] +
                                    sum_points[house]['classes'][month][klasse]['bonus'])

            dist_points.append(tmp_points)
            ov_tmp_points[house] += tmp_points
            ov_tmp_bonus[house] += tmp_bonus
            dist_bonus.append(tmp_bonus)
            dist_points_perc.append(tmp_points/(tmp_points + tmp_bonus)*100)
            dist_bonus_perc.append(tmp_bonus/(tmp_points + tmp_bonus)*100)
            ax.plot(months, line_points, linestyle='dotted', color=houses[house])
            ax.plot(months, line_overall, linestyle='solid', color=houses[house], label=house)
        ax.grid()
        ax.legend()
        ax.set_ylabel('Overall and bonus points')
        ax.set_title(klasse + ' ' + term)
        save_name = './results/plots/{term}_cls_{klasse}.png'
        plt.savefig(PurePath(save_name.format(term=term, klasse=klasse)), dpi=300)
        plt.close()

        fig, ax = plt.subplots()
        width = 0.35  # the width of the bars: can also be len(x) sequence
        ax.bar(list(houses.keys()), dist_points, width, label='Points')
        ax.bar(list(houses.keys()), dist_bonus, width, bottom=dist_points, label='Bonus')
        ax.grid(axis='y')
        ax.set_ylabel('Distribution of points')
        ax.set_title(klasse + ' ' + term)
        ax.legend()
        save_name = './results/plots/{term}_cls_{klasse}_dist.png'
        plt.savefig(PurePath(save_name.format(term=term, klasse=klasse)), dpi=300)
        plt.close()

        fig, ax = plt.subplots()
        ax.bar(list(houses.keys()), dist_points_perc, width, label='Points')
        ax.bar(list(houses.keys()), dist_bonus_perc, width, bottom=dist_points_perc, label='Bonus')
        ax.grid(axis='y')
        ax.set_ylabel('Distribution of points [perc]')
        ax.set_title(klasse + ' ' + term)
        ax.legend()
        save_name = './results/plots/{term}_cls_{klasse}_dist_perc.png'
        plt.savefig(PurePath(save_name.format(term=term, klasse=klasse)), dpi=300)
        plt.close()
    ov_dist_points = []
    ov_dist_bonus = []
    ov_dist_points_perc = []
    ov_dist_bonus_perc = []
    for house in houses:
        ov_dist_points.append(ov_tmp_points[house])
        ov_dist_bonus.append(ov_tmp_bonus[house])
        ov_dist_points_perc.append(ov_tmp_points[house]/(ov_tmp_points[house]+ov_tmp_bonus[house])*100)
        ov_dist_bonus_perc.append(ov_tmp_bonus[house]/(ov_tmp_points[house]+ov_tmp_bonus[house])*100)
    fig, ax = plt.subplots()
    width = 0.35  # the width of the bars: can also be len(x) sequence
    ax.bar(list(houses.keys()), ov_dist_points, width, label='Points')
    ax.bar(list(houses.keys()), ov_dist_bonus, width, bottom=ov_dist_points, label='Bonus')
    ax.grid(axis='y')
    ax.set_ylabel('Distribution of points')
    ax.set_title(term)
    ax.legend()
    save_name = './results/plots/{term}_cls_dist.png'
    plt.savefig(PurePath(save_name.format(term=term)), dpi=300)
    plt.close()

    fig, ax = plt.subplots()
    ax.bar(list(houses.keys()), ov_dist_points_perc, width, label='Points')
    ax.bar(list(houses.keys()), ov_dist_bonus_perc, width, bottom=ov_dist_points_perc, label='Bonus')
    ax.grid(axis='y')
    ax.set_ylabel('Distribution of points [perc]')
    ax.set_title(term)
    ax.legend()
    save_name = './results/plots/{term}_cls_dist_perc.png'
    plt.savefig(PurePath(save_name.format(term=term)), dpi=300)
    plt.close()

    for klasse in list_of_classes:
        bx_data = {}
        bx_data['fullterm'] = {}
        for house in houses:
            bx_data['fullterm'][house] = []
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
            colums = []
            for house in houses:
                colums.append(bx_data[month][house])
                bx_data['fullterm'][house].extend(bx_data[month][house])
            save_name = './results/plots/{term}_bx_cls_{klasse}_{m}.png'
            save_name = PurePath(save_name.format(term=term, klasse=klasse, m=month))
            create_bxplt(colums, klasse + ' ' + term + ' ' + month, save_name)
        colums = []
        for house in houses:
            colums.append(bx_data['fullterm'][house])
        save_name = './results/plots/{term}_bx_cls_{klasse}.png'
        save_name = PurePath(save_name.format(term=term, klasse=klasse))
        create_bxplt(colums, klasse + ' ' + term, save_name)


def create_bxplt(colums, title, filename):
    fig, ax = plt.subplots()
    box = ax.boxplot(colums, notch=True, patch_artist=True)
    for patch, house in zip(box['boxes'], houses):
        patch.set_facecolor(houses[house])
    ax.set_xticks([1, 2, 3, 4], houses, rotation=0)
    ax.grid(axis='y')
    ax.set_ylabel('Points per student')
    ax.set_title(title)
    plt.savefig(filename, dpi=300)
    plt.close()


def main():
    with open(PurePath('./results/students.json'), 'r') as fileobj:
        students = json.load(fileobj)
    with open(PurePath('./results/sum_points.json'), 'r') as fileobj:
        sum_points = json.load(fileobj)
    draw_classes(sum_points, students)


if __name__ == '__main__':
    main()
