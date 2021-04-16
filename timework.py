import pandas as pd
from datetime import date


def timeWork(claster, stDay, endDay, stYear, endYear, stMonth, endMonth, filecl):
    cols = ['DATE', 'WORKTIME']
    timedict = []
    daterange = pd.date_range(date(stYear, stMonth, stDay), date(endYear, endMonth, endDay))
    # Изменить форму обработки, годовой отчет нельзя сделать нихуя не покажет, если задать не последовательные месяца
    for single_date in daterange:
        nms = ['time', 'deadtime', 'temp']
        for i in range(16):
            nms.append("e%s" % (i + 1))
            nms.append("n%s" % (i + 1))
        try:
            timelist = []
            timework = pd.read_csv(
                '{}\\nv\\{}p{:02}-{:02}.{:02}'.format(filecl,
                                                      claster,
                                                      single_date.date().month,
                                                      single_date.date().day,
                                                      single_date.date().year - 2000),
                sep=' ',
                header=None, skipinitialspace=True)
            timework = timework.dropna(axis=1, how='all')
            timework.columns = nms
            timelist.append(
                '{:02}/{:02}/{}'.format(single_date.date().month, single_date.date().day, single_date.date().year))
            timelist.append(round(len(timework.index) * 5 / 60, 2))
            timedict.append(timelist)
        except:
            print("такого файла нит {}p{:02}-{:02}.{:02}".format(claster, single_date.date().month,
                                                                 single_date.date().day,
                                                                 single_date.date().year - 2000))
    df = pd.DataFrame(timedict, columns=cols)
    df['DATE'] = pd.to_datetime(df["DATE"])
    return df
