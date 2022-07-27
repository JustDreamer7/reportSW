from ntozeromas import ntozerotr
from datetime import date


def mask_n(stday, endday, styear, endyear, stmonth, endmonth, file1cl, file2cl):
    nto0tr = ntozerotr('', stday, endday, styear, endyear, stmonth, endmonth, file1cl)
    nto0tr_2 = ntozerotr(2, stday, endday, styear, endyear, stmonth, endmonth, file2cl)

    file = open(f'C:\\Users\\pad_z\\OneDrive\\Рабочий стол\\PrismaPassport\\Маски нейтронов\\1-й кластер - {styear} - {endyear}.txt', "a")
    file.write(f"НЕЙТРОННАЯ МАСКА {styear} - {endyear} \n")
    for i in range(1, 17):
            file.write(f'{i}-й детектор - ')
            file.write((', ').join([str(i) for i in nto0tr[nto0tr[f'n{i}'] > 0.1]['DATE'].tolist()]) + "\n")
    file.close()
    file_2 = open(f'C:\\Users\\pad_z\\OneDrive\\Рабочий стол\\PrismaPassport\\Маски нейтронов\\2-й кластер - {styear} - {endyear}.txt', "a")
    file_2.write(f"НЕЙТРОННАЯ МАСКА {styear} - {endyear} \n")
    for i in range(1, 17):
        file_2.write(f'{i}-й детектор - ')
        file_2.write((', ').join([str(i) for i in nto0tr_2[nto0tr_2[f'n{i}'] > 0.1]['DATE'].tolist()]) + "\n")
    file_2.close()



if __name__ == "__main__":
    date_time_start = date(2012, 2, 1)
    date_time_stop = date(2012, 12, 31)
    mask_n(date_time_start.day, date_time_stop.day, date_time_start.year, date_time_stop.year, date_time_start.month,
           date_time_stop.month, 'D:\\PRISMA20\\P1', 'D:\\PRISMA20\\P2')
