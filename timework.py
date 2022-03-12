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
                sep='\s[-]*\s*', header=None, skipinitialspace=True, engine='python')
            timework = timework.dropna(axis=1, how='all')
            # for i in timework.index:
            #     if len(timework.iloc[i]) > 33:
            #         print(f'Индекс {i} - кол-во{len(timework.iloc[i])}')
            # Цикл для проверки количества столбцов в файле
            # print(len(nms)) В норме должно быть 35!
            timework.columns = nms
            timework = timework.sort_values(by='time')
            if len(timework['time']) > len(timework['time'].unique()):
                # вначале удаляем дубликаты, строки только из нулей или повторяющиеся строки
                timework.drop_duplicates(keep=False, inplace=True)
                # потом ищем повторяющиеся индексы и проверяем, если в строке, кроме повтор. индекса почти одни нули
                # то удаляем и эти строки (проверяем пересечением множеств), если нет, то это просто другое событие с тем же
                # индексом
                null_row = dict(timework.isin([0, '.']).sum(axis=1))
                all_null_index = list({key: value for key, value in null_row.items() if value == 35}.keys())
                timework.drop(index=all_null_index, inplace=True)
                null_index = list({key: value for key, value in null_row.items() if value > 30}.keys())
                same_index = dict(timework['time'].duplicated(keep=False))
                same_index_row = list({key: value for key, value in same_index.items() if value == True}.keys())
                bad_index = list(set(null_index) & set(same_index_row))
                timework.drop(index=bad_index, inplace=True)
            timelist.append(
                '{:02}/{:02}/{}'.format(single_date.date().month, single_date.date().day, single_date.date().year))
            # if (len(timework['time'])) > 288:
            #     print(timework['time'].tolist())
            # print(len(timework['time']))
            # print('{:02}/{:02}/{}'.format(single_date.date().month, single_date.date().day, single_date.date().year))
            # print(round(len(timework.index) * 5 / 60, 2))
            timelist.append(round(len(timework.index) * 5 / 60, 2))
            timedict.append(timelist)
        except FileNotFoundError:
            print("такого файла нит {}p{:02}-{:02}.{:02}".format(claster, single_date.date().month,
                                                                 single_date.date().day,
                                                                 single_date.date().year - 2000))
    df = pd.DataFrame(timedict, columns=cols)
    df['DATE'] = pd.to_datetime(df["DATE"])
    return df
