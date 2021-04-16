from math import floor
import pandas as pd
from datetime import date


def timeBreak(claster, stDay, endDay, stYear, endYear, stMonth, endMonth, filecl):
    cols = ['DATE', 'stHour', 'stMinutes', 'endHour', 'endMinutes']
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
            timestop = pd.read_csv(
                '{}\\nv\\{}p{:02}-{:02}.{:02}'.format(filecl, claster,
                                                      single_date.date().month,
                                                      single_date.date().day,
                                                      single_date.date().year - 2000),
                sep=' ', header=None, skipinitialspace=True)
            timestop = timestop.dropna(axis=1, how='all')
            timestop.columns = nms
            indx = timestop['time'].tolist()
            if max(indx) != 287:
                stHour = floor(max(indx) * 5 / 60)
                stMinutes = max(indx) * 5 - stHour * 60
                endHour = 24
                endMinutes = 0
                timelist.append('{:02}/{:02}/{}'.format(single_date.date().month,
                                                        single_date.date().day,
                                                        single_date.date().year))
                timelist.append(stHour)
                timelist.append(stMinutes)
                timelist.append(endHour)
                timelist.append(endMinutes)
                timedict.append(timelist)
            if min(indx) != 0:
                stHour = 0
                stMinutes = 5
                endHour = floor(min(indx) * 5 / 60)
                endMinutes = min(indx) * 5 - endHour * 60
                timelist.append('{:02}/{:02}/{}'.format(single_date.date().month,
                                                        single_date.date().day,
                                                        single_date.date().year))
                timelist.append(stHour)
                timelist.append(stMinutes)
                timelist.append(endHour)
                timelist.append(endMinutes)
                timedict.append(timelist)
            for i in range(1, len(indx)):
                if indx[i] - indx[i - 1] > 1:
                    stHour = floor(indx[i - 1] * 5 / 60)
                    stMinutes = indx[i - 1] * 5 - stHour * 60
                    endHour = floor(indx[i] * 5 / 60)
                    endMinutes = indx[i] * 5 - endHour * 60
                    timelist.append('{:02}/{:02}/{}'.format(single_date.date().month,
                                                            single_date.date().day,
                                                            single_date.date().year))
                    timelist.append(stHour)
                    timelist.append(stMinutes)
                    timelist.append(endHour)
                    timelist.append(endMinutes)
                    timedict.append(timelist)
        except:
            print("такого файла нит {}p{:02}-{:02}.{}".format(claster, single_date.date().month,
                                                              single_date.date().day,
                                                              single_date.date().year - 2000))
    df = pd.DataFrame(timedict, columns=cols)
    df['DATE'] = pd.to_datetime(df["DATE"])
    return df
