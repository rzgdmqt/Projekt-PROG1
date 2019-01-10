from orodja import *


# download_more_pages(int(input("Koliko strani želiš analizirati? (na strani je 100 knjig): ")),
#                     goodreads_frontpage_url, directory_write, frontpage_filename)
# write_books_to_csv()
download_book_site()
download_author_page()
write_authors_to_csv()
write_book_site_to_csv()


slovarji1 = []
slovarji2 = []
path1 = os.path.join(directory_write, csv_all)
path2 = os.path.join(directory_write, csv_each)
paths = [path1, path2]
for path in paths:
    with open(path, "r", encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if path == path1:
                slovarji1.append(row)
            else:
                slovarji2.append(row)

zadnji_slovarji = []
for slovar1 in slovarji1:
    for slovar2 in slovarji2:
        if slovar1["ID_knjige"] == slovar2["ID_knjige"]:
            a = merge_dicts(slovar1, slovar2)
            del a["url_knjige"]
            del a["url_avtorja"]
            del a["avtor"]
            zadnji_slovarji.append(a)
            slovarji2.remove(slovar2)
            break


vrstice = zadnji_slovarji
header = []
for slovar in vrstice:
    slovar["koliko_ocen"] = abs(int(slovar["koliko_ocen"].replace(',', '')))
    slovar["tocke"] = int(slovar["tocke"].replace(',', ''))
    slovar["stevilo_glasov"] = abs(int(slovar["stevilo_glasov"].replace(',', '')))


for i in vrstice[0].keys():
    header.append(str(i))
write_csv(header, vrstice, directory_write, csv_books)
