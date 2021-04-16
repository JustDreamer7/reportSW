import pandas as pd
from matplotlib import pyplot as plt
import numpy as np
from shadow import shadow
from cycler import cycler
from a50more import a50more
import os



def n7Proccesing(stday, stmonth, styear, endday, endmonth, endyear, path, pathpic, file1cl, file2cl):
    datedirect = pathpic + '/{}'.format(styear)
    if ~os.path.exists(datedirect):
        try:
            os.mkdir(datedirect)
        except OSError:
            print("Создать директорию %s не удалось" % datedirect)
        else:
            print("Успешно создана директория %s " % datedirect)
    your_format = lambda x: '{{:0.{}f}}'.format(2 if x > 1 else 3).format(x)
    pd.set_option('display.float_format', your_format)
    shadowEl = shadow('', stday, endday, styear, endyear, stmonth, endmonth, file1cl)
    shadowEl2 = shadow('2', stday, endday, styear, endyear, stmonth, endmonth, file2cl)

    def gr_n7ampl(data, claster):
        plt.figure(figsize=(18, 10))
        plt.xlabel('Амплитуд, код АЦП', fontsize=20)
        plt.yscale('log')
        plt.xscale('log')
        plt.minorticks_on()
        plt.tick_params(axis='both', which='minor', direction='out', length=10, width=2, pad=10)
        plt.tick_params(axis='both', which='major', direction='out', length=20, width=4, pad=10)
        plt.xlim([1, 200])
        plt.ylim([1, 2000])
        for i in range(1, 17):
            plt.plot(data['e%s' % i].value_counts().sort_index().keys().tolist(), data['e%s' % i].value_counts(),
                     label='1',
                     marker='s', markersize=10, linewidth=5)
        plt.savefig(
            '{}\\{}\\{}n7ampl{}-{}-{}-{}.png'.format(pathpic, styear, claster, stday, stmonth, endday, endmonth),
            bbox_inches='tight')

    font = {'weight': 'bold',
            'size': 14}

    plt.rc('font', **font)
    plt.rc('axes', prop_cycle=(cycler('color', ['r', 'g', 'b', 'darkblue', 'lawngreen', 'b', 'c', 'y', 'm', 'orange',
                                                'burlywood', 'darkmagenta', 'grey', 'darkslategray', 'saddlebrown',
                                                'purple'])))

    gr_n7ampl(shadowEl, '')
    gr_n7ampl(shadowEl2, '2')



    amore = a50more('', stday, endday, styear, endyear, stmonth, endmonth, file1cl)
    amore2 = a50more('2', stday, endday, styear, endyear, stmonth, endmonth, file2cl)

    def MergingFrames(n7, n12):
        cols = ['DATE', 'TIME7', 'TIME12']
        for k in range(1, 17):
            cols.append('e%s_7' % k)
            cols.append('e%s_12' % k)
        lst_dict = []
        for i in n12['TIME']:
            for j in n7['TIME']:
                if abs(float(i) - float(j)) < 0.15:
                    dx = n12.loc[n12['TIME'] == i]
                    dy = n7.loc[n7['TIME'] == j]
                    if dx['DATE'].tolist()[0] == dy['DATE'].tolist()[0]:
                        # print('test')
                        vals = [dx['DATE'].tolist()[0], float(j), float(i)]
                        for k in range(1, 17):
                            vals.append(dy['e%s' % k].tolist()[0])
                            vals.append(dx['e%s' % k].tolist()[0])
                        lst_dict.append(dict(zip(cols, vals)))
        return pd.DataFrame(lst_dict)
    merge = MergingFrames(shadowEl,amore)
    merge2= MergingFrames(shadowEl2,amore2)

    def kproccesing(claster):
        means = []
        for i in range(1, 17):
            detlist = sorted(claster[claster['e%s_7' % i] >= 1]['e%s_7' % i].unique().tolist())
            if len(detlist) == 0:
                detlist.append(1000000000)
            means.append(detlist)
            once = []
            for item in detlist:
                once.append(claster[claster['e%s_7' % i] == item]['e%s_12' % i].mean())
            if pd.isnull(once[0]):
                means.append([-1000000000])
            else:
                means.append(once)
        for i in range(1, len(means), 2):
            print(str(i) + "-" + str(means[i - 1]))
            print(str(i + 1) + "-" + str(means[i]))
        realval = []
        labels = []
        for i in range(0, len(means), 2):
            if len(means[i]) >= 2 and np.sum(means[i]) > 3:
                realval.append(means[i])
                realval.append(means[i + 1])
                labels.append(round(i / 2) + 1)
        div = []
        fity = []
        for j in range(1, len(realval), 2):
            once = []
            for i in range(len(realval[j])):
                once.append(realval[j][i] / realval[j - 1][i])
            fity.append(np.mean(once))
            div.append(once)
        return realval, labels, div, fity

    realval, labels, div, fity = kproccesing(merge)
    realval2, labels2, div2, fity2 = kproccesing(merge2)

    def gr_kcounter(claster, realval, labels, div, fity):
        plt.figure(figsize=(18, 10))
        plt.xlabel('e1_7', fontsize=20)
        plt.ylabel('e1_12/e1_7', fontsize=20)
        plt.minorticks_on()
        plt.ylim([0, 100])
        plt.xlim([0, 40])
        plt.tick_params(axis='both', which='minor', direction='out', length=10, width=2, pad=10)
        plt.tick_params(axis='both', which='major', direction='out', length=20, width=4, pad=10)
        for i in range(len(div)):
            plt.scatter(realval[2 * i], div[i], label=labels[i], color='black', s=50)
            plt.hlines(fity[i], realval[2 * i][0], realval[2 * i][-1], color='black')
        plt.legend(bbox_to_anchor=(1.04, 1), loc="upper left")
        plt.savefig('{}\\{}\\{}krecount{}-{}-{}-{}.png'.format(pathpic, styear, claster, stday, stmonth, endday, endmonth),
                    bbox_inches='tight')
        with open(f'{path}\{claster}kRecount-{stday:02}.{stmonth:02}.{styear}-{endday:02}.{endmonth:02}.{endyear}.txt',
                  'w') as f:
            for i in range(len(labels)):
                f.write(str(labels[i]) + '-' + str(round(fity[i], 3))+'\n')

    gr_kcounter('1', realval, labels, div, fity)
    gr_kcounter('2', realval2, labels2, div2, fity2)