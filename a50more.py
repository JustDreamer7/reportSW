import pandas as pd
from datetime import date


def a50more(n, stDay, endDay, stYear, endYear, stMonth, endMonth, filecl):
    cols = ['DATE', 'TIME', 'number', 'ntr', 'tr']
    filtr = range(50, 550)
    mainfiltr = []
    ecols = []

    for i in range(16):
        ecols.append("e%s" % (i + 1))
        mainfiltr.append(filtr)
        cols.append("e%s" % (i + 1))
        cols.append("n%s" % (i + 1))
    df = pd.DataFrame(columns=cols)
    daterange = pd.date_range(date(stYear, stMonth, stDay), date(endYear, endMonth, endDay))
    # Изменить форму обработки, годовой отчет нельзя сделать нихуя не покажет, если задать не последовательные месяца
    for single_date in daterange:
        nms = ['TIME', 'number', 'ntr', 'tr']
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
                sep=' ', header=None, skipinitialspace=True)
            a_fr4 = a_fr4.dropna(axis=1, how='all')
            a_fr4.columns = nms

            a_fr4['fr_sum'] = a_fr4.isin(dict(zip(ecols, mainfiltr))).sum(axis=1, skipna=True)
            a_fr4 = a_fr4[a_fr4['fr_sum'] >= 1]
            a_fr4['DATE'] = ['{:02}/{:02}/{}'.format(single_date.date().month,
                                                     single_date.date().day,
                                                     single_date.date().year)] * len(a_fr4.index)
            # a_fr4 = a_fr4[ecols]
            df = pd.concat([df, a_fr4], ignore_index=True)
        except:
            print("такого файла нит {}n{:02}-{:02}.{:02}".format(n, single_date.date().month,
                                                                 single_date.date().day,
                                                                 single_date.date().year - 2000))
    df['DATE'] = pd.to_datetime(df["DATE"])
    print(df)
    if df['TIME'].dtypes == 'object':
        df['TIME'] = df['TIME'].str.replace(',', '.')
    return df
