import pandas as pd
from datetime import date
import sqlalchemy
from matplotlib import pyplot as plt

from a52det import a52det


def make_event(df, df_mask, amp, fr):
    """Применяем маску, то есть зануляем все значения, в нерабочих детекторах"""
    df_mask['DATE'] = df_mask['date']
    df_mask = df_mask.drop('date', axis=1)
    make_date = []
    for i in df['DATE']:
        make_date.append(i.date())
    df['DATE'] = make_date
    df = df.merge(df_mask)
    # print(df_mask['DATE'])
    # print(df['DATE'])
    filtr = range(amp, 550)
    ecols = []
    for i in range(16):
        df.loc[df[df[
                      f'amp{i + 1}_mask'] == 0].index, f'e{i + 1}'] = 0  # Место применения маски, впереди лишь форматирование
        df.loc[df[df[f'n{i + 1}_mask'] == 0].index, f'n{i + 1}'] = 0
    for i in range(16):
        ecols.append("e%s" % (i + 1))
    eframe1 = pd.DataFrame(df[ecols])
    eframe1['fr_sum'] = eframe1.isin(filtr).sum(axis=1, skipna=True)
    corr_df1 = df.loc[eframe1[eframe1['fr_sum'] >= fr].index, :]
    corr_df1.reset_index(drop=True)
    # print(corr_df1)
    return corr_df1


def main(start_date, end_date, amp, fr):
    conn = 'postgresql+psycopg2://postgres:qwerty@localhost:5432/prisma'
    engine = sqlalchemy.create_engine(conn)
    connect = engine.connect()
    mask_prisma_1 = pd.read_sql("SELECT * FROM mask_1_params WHERE date >= '{}-{:02}-{:02}' AND  date <= \
               '{}-{:02}-{:02}' ORDER BY date asc;".format(start_date.year, start_date.month, start_date.day,
                                                           end_date.year,
                                                           end_date.month, end_date.day), connect)
    mask_prisma_2 = pd.read_sql(
        "SELECT * FROM mask_2_params  WHERE date >= '{}-{:02}-{:02}' AND  date <= \
        '{}-{:02}-{:02}' ORDER BY date asc;".format(start_date.year, start_date.month, start_date.day, end_date.year,
                                                    end_date.month, end_date.day), connect)
    data_prisma_1 = a52det('', start_date.day, end_date.day, start_date.year, end_date.year, start_date.month,
                           end_date.month, filecl='D:\\PRISMA20\\P1', amp=11, fr=1)
    data_prisma_2 = a52det(2, start_date.day, end_date.day, start_date.year, end_date.year, start_date.month,
                           end_date.month, filecl='D:\\PRISMA20\\P2', amp=11, fr=1)

    corr_df1 = make_event(data_prisma_1, mask_prisma_1, amp=amp,
                          fr=fr)  # Применяем маски, оставляем лишь события с фильтром
    corr_df2 = make_event(data_prisma_2, mask_prisma_2, amp=amp, fr=fr)
    corr_df1['DATE'] = pd.to_datetime(corr_df1["DATE"])
    corr_df2['DATE'] = pd.to_datetime(corr_df2["DATE"])
    return corr_df1, corr_df2

if __name__ == "__main__":
    # neutron_data_missed("2018-05-17")

    date_time_start = date(2013, 1, 18)
    date_time_stop = date(2014, 12, 31)
    main(date_time_start, date_time_stop, 11, 1)
    print('test')
