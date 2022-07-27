import pandas as pd
from datetime import date


def a4fr(n, stDay, endDay, stYear, endYear, stMonth, endMonth, filecl):
    cols = ['DATE', 'EVENTS']
    filtr = range(5, 550)
    ecols = []
    for i in range(16):
        ecols.append("e%s" % (i + 1))
    timedict = []
    daterange = pd.date_range(date(stYear, stMonth, stDay), date(endYear, endMonth, endDay))
    # Изменить форму обработки, годовой отчет нельзя сделать нихуя не покажет, если задать не последовательные месяца
    for single_date in daterange:
        nms = ['time', 'number', 'ntr', 'tr']
        for i in range(16):
            nms.append("e%s" % (i + 1))
            nms.append("n%s" % (i + 1))
        try:
            a_fr4list = []
            a_fr4 = pd.read_csv(
                '{}\\{}n_{:02}-{:02}.{:02}'.format(filecl, n,
                                                      single_date.date().month,
                                                      single_date.date().day,
                                                      single_date.date().year - 2000),
                sep=' ',
                header=None, skipinitialspace=True)
            a_fr4 = a_fr4.dropna(axis=1, how='all')
            a_fr4.columns = nms
            eframe = pd.DataFrame(a_fr4[ecols])
            eframe['fr_sum'] = eframe.isin(filtr).sum(axis=1, skipna=True)
            a_fr4list.append('{:02}/{:02}/{}'.format(single_date.date().month,
                                                     single_date.date().day,
                                                     single_date.date().year))
            a_fr4list.append(len(eframe[eframe['fr_sum'] >= 4].index))
            timedict.append(a_fr4list)
        except:
            a_fr4list = []
            a_fr4list.append('{:02}/{:02}/{}'.format(single_date.date().month,
                                                     single_date.date().day,
                                                     single_date.date().year))
            a_fr4list.append(0.00)
            timedict.append(a_fr4list)
            print("такого файла нит {}n{:02}-{:02}.{:02}".format(n, single_date.date().month,
                                                                 single_date.date().day,
                                                                 single_date.date().year - 2000))
    df = pd.DataFrame(timedict, columns=cols)
    df['DATE'] = pd.to_datetime(df["DATE"])
    return df
