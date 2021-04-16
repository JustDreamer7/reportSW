import pandas as pd
from datetime import date


def shadow(claster, n, stDay, endDay, stYear, endYear, stMonth, endMonth):
    cols = ['DATE', 'TIME', 'number', 'tr']

    for i in range(16):
        cols.append("e%s" % (i + 1))

    df = pd.DataFrame(columns=cols)
    daterange = pd.date_range(date(stYear, stMonth, stDay), date(endYear, endMonth, endDay))
    # Изменить форму обработки, годовой отчет нельзя сделать нихуя не покажет, если задать не последовательные месяца
    for single_date in daterange:
        nms = ['TIME', 'number', 'tr']
        for i in range(16):
            nms.append("e%s" % (i + 1))
        try:
            a_fr4list = []
            a_fr4 = pd.read_csv(
                'C:\\Users\\JustDreamer\\Desktop\\PRISMA\\P{}_7\\{}n7_{:02}-{:02}.{:02}'.format(claster, n,
                                                                                                single_date.date().month,
                                                                                                single_date.date().day,
                                                                                                single_date.date().year - 2000),
                sep=' ', header=None, skipinitialspace=True)
            a_fr4 = a_fr4.dropna(axis=1, how='all')
            a_fr4.columns = nms
            a_fr4['DATE'] = ['{:02}/{:02}/{}'.format(single_date.date().month,
                                                     single_date.date().day,
                                                     single_date.date().year)] * len(a_fr4.index)
            a_fr4 = a_fr4[cols]
            df = pd.concat([df, a_fr4], ignore_index=True)
        except:
            print("такого файла нит {}n7{:02}-{:02}.{:02}".format(n, single_date.date().month,
                                                                 single_date.date().day,
                                                                 single_date.date().year - 2000))
    df['DATE'] = pd.to_datetime(df["DATE"])
    if df['TIME'].dtypes == 'object':
        df['TIME'] = df['TIME'].str.replace(',', '.')
    print(df)
    return df