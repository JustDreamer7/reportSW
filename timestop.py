import datetime
from math import floor
import pandas as pd
from datetime import date


def timeBreak(claster, stDay, endDay, stYear, endYear, stMonth, endMonth, filecl):
    cols = ['DATE', 'stHour', 'stMinutes', 'endHour', 'endMinutes']
    timedict = []
    daterange = pd.date_range(date(stYear, stMonth, stDay), date(endYear, endMonth, endDay))
    # Изменить форму обработки, годовой отчет нельзя сделать нихуя не покажет, если задать не последовательные месяца
    for single_date in daterange:
        #     if single_date.date() < date(2013, 1, 18):
        #         nms = ['time', 'deadtime']
        #     else:
        #         nms = ['time', 'deadtime', 'temp']
        #     for i in range(16):
        #         nms.append("e%s" % (i + 1))
        #         nms.append("n%s" % (i + 1))
        try:
            timestop = pd.read_csv(
                '{}\\nv\\{}p{:02}-{:02}.{:02}'.format(filecl, claster,
                                                      single_date.date().month,
                                                      single_date.date().day,
                                                      single_date.date().year - 2000),
                sep='\s[-]*\s*', header=None, skipinitialspace=True, engine='python')
            # error_bad_lines=False, warn_bad_lines=True
            timestop = timestop.dropna(axis=1, how='all')
            # timestop.columns = nms
            timestop['time'] = timestop[0]
            del timestop[0]
            timestop = timestop.sort_values(by='time')
            # single_date.date() <= datetime.date(2013, 9, 3) and
            if (288 in timestop['time'].tolist()) and (0 not in timestop['time'].tolist()):
                timestop['time'] = [i - 1 for i in timestop['time'].tolist()]
            #     single_date.date() <= datetime.date(2013, 8, 22) and
            # if claster == 2 and (288 in timestop['time']):
            #     timestop['time'] = [i-1 for i in timestop['time'].tolist()]
            # Более поздняя вставка, нужная для того, чтобы обрабатывать ранние файлы призмы с багами в записи
            # Баги в виде строк из нулей
            if len(timestop['time']) > len(timestop['time'].unique()):
                print(f'timestop.columns - {timestop.columns}')
                if len(timestop.columns) == 35:
                    # вначале удаляем дубликаты, строки только из нулей или повторяющиеся строки
                    timestop.drop_duplicates(keep=False, inplace=True)
                    # потом ищем повторяющиеся индексы и проверяем, если в строке, кроме повтор. индекса почти одни нули
                    # то удаляем и эти строки (проверяем пересечением множеств), если нет, то это просто другое событие с тем же
                    # индексом
                    null_row = dict(timestop.isin([0, '.']).sum(axis=1))
                    all_null_index = list({key: value for key, value in null_row.items() if value == 35}.keys())
                    timestop.drop(index=all_null_index, inplace=True)
                    null_index = list({key: value for key, value in null_row.items() if value > 30}.keys())
                    same_index = dict(timestop['time'].duplicated(keep=False))
                    same_index_row = list({key: value for key, value in same_index.items() if value == True}.keys())
                    bad_index = list(set(null_index) & set(same_index_row))
                    timestop.drop(index=bad_index, inplace=True)
                    if len(timestop.index) == 288:
                        timestop.reset_index(drop=True, inplace=True)
                        timestop['time'] = timestop.index
                    same_index = dict(timestop['time'].eq(timestop['time'].shift()))
                    same_index_row = list({key: value for key, value in same_index.items() if value == True}.keys())
                    # Надо нормально менять стоблец с временем, чтобы индексы были расставлены правильно.
                    while len(same_index_row) != 0:
                        change = list(timestop['time'])
                        for i in range(1, len(change)):
                            if change[i - 1] == change[i]:
                                change[i] = change[i] + 1
                        timestop['time'] = change
                        same_index = dict(timestop['time'].eq(timestop['time'].shift()))
                        same_index_row = list({key: value for key, value in same_index.items() if value == True}.keys())
                    if len(timestop.index) == 289:
                        timestop = timestop.head(288)
                elif len(timestop.columns) == 34:
                    # вначале удаляем дубликаты, строки только из нулей или повторяющиеся строки
                    timestop.drop_duplicates(keep=False, inplace=True)
                    # потом ищем повторяющиеся индексы и проверяем, если в строке, кроме повтор. индекса почти одни нули
                    # то удаляем и эти строки (проверяем пересечением множеств), если нет, то это просто другое событие с тем же
                    # индексом
                    null_row = dict(timestop.isin([0, '.']).sum(axis=1))
                    all_null_index = list({key: value for key, value in null_row.items() if value == 34}.keys())
                    timestop.drop(index=all_null_index, inplace=True)
                    null_index = list({key: value for key, value in null_row.items() if value > 29}.keys())
                    same_index = dict(timestop['time'].duplicated(keep=False))
                    same_index_row = list({key: value for key, value in same_index.items() if value == True}.keys())
                    bad_index = list(set(null_index) & set(same_index_row))
                    timestop.drop(index=bad_index, inplace=True)
                    if len(timestop.index) == 288:
                        timestop.reset_index(drop=True, inplace=True)
                        timestop['time'] = timestop.index
                    same_index = dict(timestop['time'].eq(timestop['time'].shift()))
                    same_index_row = list({key: value for key, value in same_index.items() if value == True}.keys())
                    # Надо нормально менять стоблец с временем, чтобы индексы были расставлены правильно.
                    while len(same_index_row) != 0:
                        change = list(timestop['time'])
                        for i in range(1, len(change)):
                            if change[i - 1] == change[i]:
                                change[i] = change[i] + 1
                        timestop['time'] = change
                        same_index = dict(timestop['time'].eq(timestop['time'].shift()))
                        same_index_row = list(
                            {key: value for key, value in same_index.items() if value == True}.keys())
                        if len(timestop.index) == 289:
                            timestop = timestop.head(288)

                elif len(timestop.columns) == 33:
                    # вначале удаляем дубликаты, строки только из нулей или повторяющиеся строки
                    timestop.drop_duplicates(keep=False, inplace=True)
                    # потом ищем повторяющиеся индексы и проверяем, если в строке, кроме повтор. индекса почти одни нули
                    # то удаляем и эти строки (проверяем пересечением множеств), если нет, то это просто другое событие с тем же
                    # индексом
                    null_row = dict(timestop.isin([0, '.']).sum(axis=1))
                    all_null_index = list({key: value for key, value in null_row.items() if value == 34}.keys())
                    timestop.drop(index=all_null_index, inplace=True)
                    null_index = list({key: value for key, value in null_row.items() if value > 29}.keys())
                    same_index = dict(timestop['time'].duplicated(keep=False))
                    same_index_row = list({key: value for key, value in same_index.items() if value == True}.keys())
                    bad_index = list(set(null_index) & set(same_index_row))
                    timestop.drop(index=bad_index, inplace=True)
                    if len(timestop.index) == 288:
                        timestop.reset_index(drop=True, inplace=True)
                        timestop['time'] = timestop.index
                    same_index = dict(timestop['time'].eq(timestop['time'].shift()))
                    same_index_row = list({key: value for key, value in same_index.items() if value == True}.keys())
                    # Надо нормально менять стоблец с временем, чтобы индексы были расставлены правильно.
                    while len(same_index_row) != 0:
                        change = list(timestop['time'])
                        for i in range(1, len(change)):
                            if change[i - 1] == change[i]:
                                change[i] = change[i] + 1
                        timestop['time'] = change
                        same_index = dict(timestop['time'].eq(timestop['time'].shift()))
                        same_index_row = list(
                            {key: value for key, value in same_index.items() if value == True}.keys())
                    if len(timestop.index) == 289:
                        timestop = timestop.head(288)

                # ПОЧЕМУ БЛЯТЬ С ЭТИМ ЦИКЛОМ ТУТ ПОЧЕМУ СЧИТАЕТ МОМЕНТЫ КОГДА У НАС НЕТ ПРОБЕЛА ВО ВРЕМЕНИ
                # после удаления ненужных строк, ребутаем индексы, теперь они должны быть уникальны
                # del timestop['deadtime']
                # if single_date.date() >= date(2013, 1, 18):
                #     del timestop['temp']

                # if single_date.date().day == 1:
                #     print(len(timestop['time']))
                #     print(len(timestop['time'].unique()))
                #     print(timestop)
                # if len(timestop['time'])>len(timestop['time'].unique()):
                #     timestop = timestop.groupby('time').sum().reset_index()
            indx = timestop['time'].tolist()
            print(indx)
            if max(indx) < 287:
                timelist = []
                stHour = floor(max(indx) * 5 / 60)
                stMinutes = max(indx) * 5 - stHour * 60
                endHour = 23
                endMinutes = 55
                timelist.append('{:02}/{:02}/{}'.format(single_date.date().month,
                                                        single_date.date().day,
                                                        single_date.date().year))
                timelist.append(stHour)
                timelist.append(stMinutes)
                timelist.append(endHour)
                timelist.append(endMinutes)
                timedict.append(timelist)
            if min(indx) != 0:
                timelist = []
                stHour = 0
                stMinutes = 0
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
                    print('test')
                    timelist = []
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
    # print(df)
    return df
