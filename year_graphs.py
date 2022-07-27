import os
from datetime import date

import pandas as pd
from cycler import cycler
from matplotlib import pyplot as plt
from corr_a52det import main, make_event
from a52det import a52det
from ntozeromas import ntozerotr
from ntozeromas import change_name
from timework import timeWork



def yearGraphs(stday, stmonth, styear, endday, endmonth, endyear, pathpic, file1cl, file2cl, amp, fr):
    data, data_2 = main(start_date=date(styear, stmonth, stday), end_date=date(endyear, endmonth, endday), amp=amp,
                        fr=fr)
    nto0tr, nto0tr_2 = change_name(start_date=date(styear, stmonth, stday), end_date=date(endyear, endmonth, endday))

    # data = a52det('', stday, endday, styear, endyear, stmonth, endmonth, file1cl, amp, fr)
    # data_2 = a52det(2, stday, endday, styear, endyear, stmonth, endmonth, file2cl, amp, fr)
    # nto0tr = ntozerotr('', stday, endday, styear, endyear, stmonth, endmonth, file1cl)
    # nto0tr_2 = ntozerotr(2, stday, endday, styear, endyear, stmonth, endmonth, file2cl)

    worktime = timeWork(1, stday, endday, styear, endyear, stmonth, endmonth, file1cl)
    worktime_2 = timeWork(2, stday, endday, styear, endyear, stmonth, endmonth, file2cl)

    a = date(styear, stmonth, stday)
    b = date(endyear, endmonth, endday)

    font = {'weight': 'bold',
            'size': 50}

    plt.rc('font', **font)
    plt.rc('axes',
           prop_cycle=(cycler('color', ['r', 'g', 'b', 'darkblue', 'lawngreen', 'hotpink', 'c', 'y', 'm', 'orange',
                                        'burlywood', 'darkmagenta', 'grey', 'darkslategray', 'saddlebrown',
                                        'lightsalmon'])))
    # plt.rc('legend', fontsize=50)
    # plt.rc('legend', fontsize='large')
    plt.figure(figsize=(100, 20))
    plt.xlabel('Дата', fontsize=80)
    plt.ylabel(r'$(coб)^{-1}$', fontsize=80)
    plt.grid()
    plt.minorticks_on()
    plt.tick_params(axis='both', which='minor', direction='out', length=20, width=4, pad=15)
    plt.tick_params(axis='both', which='major', direction='out', length=40, width=6, pad=15)
    plt.grid(which='minor',
             color='k',
             linestyle=':')
    plt.ylim([0, 0.5], emit=False)
    plt.xlim([a, b])
    box_1 = {'facecolor': 'white',  # цвет области
             'edgecolor': 'red',  # цвет крайней линии
             'boxstyle': 'round'}
    plt.title("1-кластер", bbox=box_1, fontsize=50, loc='center')
    print(nto0tr['DATE'])
    for i in range(1, 17):
        plt.plot(nto0tr['DATE'], nto0tr['n%s' % i], label='%s' % i, linewidth=2)
    leg = plt.legend(bbox_to_anchor=(1.04, 1), loc="upper left")
    # get the individual lines inside legend and set line width
    for line in leg.get_lines():
        line.set_linewidth(8)
    # get label texts inside legend and set font size
    for text in leg.get_texts():
        text.set_fontsize(50)
    plt.savefig(
        '{}\\ntozeromas{}-{}-{}-{}-{}-{}.png'.format(pathpic, stday, stmonth, styear, endday, endmonth, endyear),
        bbox_inches='tight')
    nzm1path = "{}\\ntozeromas{}-{}-{}-{}-{}-{}.png".format(pathpic, stday, stmonth, styear, endday, endmonth, endyear)

    plt.figure(figsize=(100, 20))
    plt.xlabel('Дата', fontsize=80)
    plt.ylabel(r'$(coб)^{-1}$', fontsize=80)
    plt.grid()
    plt.minorticks_on()
    plt.tick_params(axis='both', which='minor', direction='out', length=20, width=4, pad=15)
    plt.tick_params(axis='both', which='major', direction='out', length=40, width=6, pad=15)
    plt.grid(which='minor',
             color='k',
             linestyle=':')
    plt.ylim([0, 0.5], emit=False)
    plt.xlim([a, b])
    box_1 = {'facecolor': 'white',  # цвет области
             'edgecolor': 'red',  # цвет крайней линии
             'boxstyle': 'round'}
    plt.title("2-кластер", bbox=box_1, fontsize=50, loc='center')
    for i in range(1, 17):
        plt.plot(nto0tr_2['DATE'], nto0tr_2['n%s' % i], label='%s' % i, linewidth=2)
    leg = plt.legend(bbox_to_anchor=(1.04, 1), loc="upper left")
    # get the individual lines inside legend and set line width
    for line in leg.get_lines():
        line.set_linewidth(8)
    # get label texts inside legend and set font size
    for text in leg.get_texts():
        text.set_fontsize(50)
    plt.savefig(
        '{}\\2ntozeromas{}-{}-{}-{}-{}-{}.png'.format(pathpic, stday, stmonth, styear, endday, endmonth, endyear),
        bbox_inches='tight')
    nzm2path = "{}\\2ntozeromas{}-{}-{}-{}-{}-{}.png".format(pathpic, stday, stmonth, styear, endday, endmonth, endyear)

    nto0tr.to_csv(
        f'C:\\Users\\pad_z\\OneDrive\\Рабочий стол\\PrismaPassport\\PRISMA year-graphs\\n_to_0\\n_to_0_1_cl_{stday}-{stmonth}-{styear}-{endday}-{endmonth}-{endyear}.csv',
        index=False, sep=';')
    nto0tr_2.to_csv(
        f'C:\\Users\\pad_z\\OneDrive\\Рабочий стол\\PrismaPassport\\PRISMA year-graphs\\n_to_0\\n_to_0_2_cl_{stday}-{stmonth}-{styear}-{endday}-{endmonth}-{endyear}.csv',
        index=False, sep=';')

    # CКОРОСТЬ СЧЕТА
    plt.figure(figsize=(100, 20))
    plt.xlabel('Дата', fontsize=80)
    plt.ylabel('N, соб/час', fontsize=80)
    plt.grid()
    plt.minorticks_on()
    plt.tick_params(axis='both', which='minor', direction='out', length=10, width=2, pad=15)
    plt.tick_params(axis='both', which='major', direction='out', length=20, width=4, pad=15)
    plt.xlim([a, b])
    plt.ylim([0, 8])
    # plt.rc('axes', prop_cycle=(cycler('color', ['r', 'g', 'b', 'darkblue', 'lawngreen', 'b', 'c', 'y', 'm', 'orange',
    #                                             'burlywood', 'darkmagenta', 'grey', 'darkslategray', 'saddlebrown',
    #                                             'purple'])))
    plt.grid(which='minor',
             color='k',
             linestyle=':')
    box_1 = {'facecolor': 'white',  # цвет области
             'edgecolor': 'red',  # цвет крайней линии
             'boxstyle': 'round'}
    plt.title("1-кластер", bbox=box_1, fontsize=50, loc='center')
    a_fr = [list(data['DATE'])]
    for i in range(1, 17):
        test = data[data['e%s' % i] > amp]['DATE'].value_counts().sort_index().to_frame()
        test['VALUE'] = test['DATE']
        test['DATE'] = test.index
        test['DATE'] = pd.to_datetime(test["DATE"])
        # print(test['DATE'])
        # print(worktime['DATE'])
        test = test.merge(worktime, how='left')
        a_fr.append(test['VALUE'] / test['WORKTIME'])
        plt.plot(test['DATE'], test['VALUE'] / test['WORKTIME'], label='%s' % i, linewidth=2)
    leg = plt.legend(bbox_to_anchor=(1.04, 1), loc="upper left")
    # get the individual lines inside legend and set line width
    for line in leg.get_lines():
        line.set_linewidth(8)
    # get label texts inside legend and set font size
    for text in leg.get_texts():
        text.set_fontsize(50)
    plt.savefig(
        '{}\\va_{}_fr_{}_{}-{}-{}-{}-{}-{}.png'.format(pathpic, amp, fr, stday, stmonth, styear, endday, endmonth,
                                                       endyear),
        bbox_inches='tight')
    # a2f5path = "{}\\va_{}_fr_{}_{}-{}-{}-{}-{}-{}.png".format(pathpic, amp, fr, stday, stmonth, styear, endday,
    #                                                           endmonth,
    #                                                           endyear)

    plt.figure(figsize=(100, 20))
    plt.xlabel('Дата', fontsize=80)
    plt.ylabel('N, соб/час', fontsize=80)
    plt.grid()
    plt.minorticks_on()
    plt.tick_params(axis='both', which='minor', direction='out', length=10, width=2, pad=15)
    plt.tick_params(axis='both', which='major', direction='out', length=20, width=4, pad=15)
    plt.xlim([a, b])
    plt.ylim([0, 8])
    plt.grid(which='minor',
             color='k',
             linestyle=':')
    box_1 = {'facecolor': 'white',  # цвет области
             'edgecolor': 'red',  # цвет крайней линии
             'boxstyle': 'round'}
    plt.title("2-кластер", bbox=box_1, fontsize=50, loc='center')
    a_fr_ver_2 = [list(data_2['DATE'])]
    for i in range(1, 17):
        test_2 = data_2[data_2['e%s' % i] > amp]['DATE'].value_counts().sort_index().to_frame()
        test_2['VALUE'] = test_2['DATE']
        test_2['DATE'] = test_2.index
        test_2['DATE'] = pd.to_datetime(test_2["DATE"])
        test_2 = test_2.merge(worktime_2, how='left')
        a_fr_ver_2.append(test_2['VALUE'] / test_2['WORKTIME'])
        plt.plot(test_2['DATE'], test_2['VALUE'] / test_2['WORKTIME'], label='%s' % i, linewidth=2)
    leg = plt.legend(bbox_to_anchor=(1.04, 1), loc="upper left")
    # get the individual lines inside legend and set line width
    for line in leg.get_lines():
        line.set_linewidth(8)
    # get label texts inside legend and set font size
    for text in leg.get_texts():
        text.set_fontsize(50)
    plt.savefig(
        '{}\\v2a_{}_fr_{}_{}-{}-{}-{}-{}-{}.png'.format(pathpic, amp, fr, stday, stmonth, styear, endday, endmonth,
                                                        endyear),
        bbox_inches='tight')
    # a2f52path = "{}\\v2a_{}_fr_{}-{}-{}-{}-{}-{}.png".format(pathpic, amp, fr, stday, stmonth, styear, endday, endmonth,
    #                                                          endyear)
    datedirect = pathpic + f'\\a_{amp}_fr_{fr}'
    if ~os.path.exists(datedirect):
        try:
            os.mkdir(datedirect)
        except OSError:
            print("Создать директорию %s не удалось" % datedirect)
        else:
            print("Успешно создана директория %s " % datedirect)
    df1 = pd.DataFrame(a_fr).T
    df2 = pd.DataFrame(a_fr_ver_2).T
    df1.to_csv(
        f'C:\\Users\\pad_z\\OneDrive\\Рабочий стол\\PrismaPassport\\PRISMA year-graphs\\a_{amp}_fr_{fr}\\a_{amp}_fr_{fr}_1_cl_{stday}-{stmonth}-{styear}-{endday}-{endmonth}-{endyear}.csv',
        index=False, sep=';', header=False)
    df2.to_csv(
        f'C:\\Users\\pad_z\\OneDrive\\Рабочий стол\\PrismaPassport\\PRISMA year-graphs\\a_{amp}_fr_{fr}\\a_{amp}_fr_{fr}_2_cl_{stday}-{stmonth}-{styear}-{endday}-{endmonth}-{endyear}.csv',
        index=False, sep=';', header=False)

    # """Code to make frame with detectors which have overrun with neutrons"""
    # nto0tr_2.index = nto0tr_2['DATE']
    # nto0tr.index = nto0tr['DATE']
    # del nto0tr['DATE']
    # del nto0tr_2['DATE']
    # nto0tr.columns = [str(i) for i in range(1, 17)]
    # nto0tr_2.columns = [str(i) for i in range(1, 17)]
    #
    # nto0tr_dict = nto0tr.gt(0.1).to_dict('index')  # Делаем словарь, где значение - True, если > 0,1.
    #                                                # Потом оставляем только их в словаре
    # for i, j in zip(nto0tr_dict.keys(), nto0tr_dict.values()):
    #     nto0tr_dict[i] = ','.join(list({key: value for key, value in j.items() if value == True}))
    #
    # nto0tr_2_dict = nto0tr_2.gt(0.1).to_dict('index')
    # for i, j in zip(nto0tr_2_dict.keys(), nto0tr_2_dict.values()):
    #     nto0tr_2_dict[i] = ','.join(list({key: value for key, value in j.items() if value == True}))
    return None


if __name__ == "__main__":
    date_time_start = date(2015, 1, 1)
    date_time_stop = date(2015, 12, 31)
    yearGraphs(date_time_start.day, date_time_start.month, date_time_start.year, date_time_stop.day,
               date_time_stop.month, date_time_stop.year, file1cl='D:\\PRISMA20\\P1',
               file2cl='D:\\PRISMA20\\P2', amp=11,
               pathpic='C:\\Users\\pad_z\\OneDrive\\Рабочий стол\\PrismaPassport\\PRISMA year-graphs', fr=1)
    print('test')
