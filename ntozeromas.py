import pandas as pd
from datetime import date
import sqlalchemy


def ntozerotr(n, stDay, endDay, stYear, endYear, stMonth, endMonth, filecl):
    cols = ['DATE']
    for i in range(16):
        cols.append("n%s" % (i + 1))
    timedict = []
    daterange = pd.date_range(date(stYear, stMonth, stDay), date(endYear, endMonth, endDay))
    for single_date in daterange:
        nms = ['time', 'number', 'ntr', 'tr']
        for i in range(16):
            nms.append("e%s" % (i + 1))
            nms.append("n%s" % (i + 1))
        try:
            ntrbyzrtr = []
            nto0tr = pd.read_csv(
                '{}\\{}n_{:02}-{:02}.{:02}'.format(filecl, n,
                                                   single_date.date().month,
                                                   single_date.date().day,
                                                   single_date.date().year - 2000),
                sep=' ', header=None, skipinitialspace=True)
            nto0tr = nto0tr.dropna(axis=1, how='all')
            nto0tr.columns = nms
            zerotr = len(nto0tr[nto0tr['tr'] == 0].index)
            zeroframe = nto0tr[nto0tr['tr'] == 0]
            ntrbyzrtr.append('{:02}/{:02}/{}'.format(single_date.date().month,
                                                     single_date.date().day,
                                                     single_date.date().year))
            for i in range(16):
                ntrbyzrtr.append(round(zeroframe["n%s" % (i + 1)].sum() / zerotr, 3))
            timedict.append(ntrbyzrtr)
        except:
            ntrbyzrtr = []
            ntrbyzrtr.append('{:02}/{:02}/{}'.format(single_date.date().month,
                                                     single_date.date().day,
                                                     single_date.date().year))
            for i in range(16):
                ntrbyzrtr.append(0.00)
            timedict.append(ntrbyzrtr)
            print("такого файла нит {}n{:02}-{:02}.{:02}".format(n, single_date.date().month,
                                                                 single_date.date().day,
                                                                 single_date.date().year - 2000))
    df = pd.DataFrame(timedict, columns=cols)
    df['DATE'] = pd.to_datetime(df["DATE"])
    return df


def change_name(start_date, end_date):
    conn = 'postgresql+psycopg2://postgres:qwerty@localhost:5432/prisma'
    engine = sqlalchemy.create_engine(conn)
    connect = engine.connect()
    mask_prisma_1 = pd.read_sql("SELECT * FROM mask_1_params WHERE date >= '{}-{:02}-{:02}' AND  date < \
               '{}-{:02}-{:02}' ORDER BY date asc;".format(start_date.year, start_date.month, start_date.day,
                                                           end_date.year,
                                                           end_date.month, end_date.day), connect)
    mask_prisma_2 = pd.read_sql(
        "SELECT * FROM mask_2_params  WHERE date >= '{}-{:02}-{:02}' AND  date < \
        '{}-{:02}-{:02}' ORDER BY date asc;".format(start_date.year, start_date.month, start_date.day, end_date.year,
                                                    end_date.month, end_date.day), connect)
    data_prisma_1 = ntozerotr('', start_date.day, end_date.day, start_date.year, end_date.year, start_date.month,
                              end_date.month, 'D:\\PRISMA20\\P1')
    data_prisma_2 = ntozerotr(2, start_date.day, end_date.day, start_date.year, end_date.year, start_date.month,
                              end_date.month, 'D:\\PRISMA20\\P2')
    corr_df1 = make_event(data_prisma_1, mask_prisma_1)
    corr_df2 = make_event(data_prisma_2, mask_prisma_2)
    corr_df1['DATE'] = pd.to_datetime(corr_df1["DATE"])
    corr_df2['DATE'] = pd.to_datetime(corr_df2["DATE"])
    return corr_df1, corr_df2

def make_event(df, df_mask):
    """Применяем маску, то есть зануляем все значения, в нерабочих детекторах"""
    df_mask['DATE'] = df_mask['date']
    df_mask = df_mask.drop('date', axis=1)
    make_date = []
    for i in df['DATE']:
        make_date.append(i.date())
    df['DATE'] = make_date
    df = df.merge(df_mask)
    for i in range(16):
        df.loc[df[df[f'n{i + 1}_mask'] == 0].index, f'n{i + 1}'] = 0
    corr_df1 = df
    corr_df1.reset_index(drop=True)
    return corr_df1
