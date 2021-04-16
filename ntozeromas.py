import pandas as pd
from datetime import date


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
                '{}\\n\\{}n_{:02}-{:02}.{:02}'.format(filecl, n,
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
            print("такого файла нит {}n{:02}-{:02}.{:02}".format(n, single_date.date().month,
                                                                 single_date.date().day,
                                                                 single_date.date().year - 2000))
    df = pd.DataFrame(timedict, columns=cols)
    df['DATE'] = pd.to_datetime(df["DATE"])
    return df
