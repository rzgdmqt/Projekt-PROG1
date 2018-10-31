import re
import os
import csv


directory = r'C:\Users\MasterX\Desktop\UVP\Projekt-PROG1\html_strani_in_csv'
directory_knjige = r'C:\Users\MasterX\Desktop\UVP\Projekt-PROG1\html_strani_in_csv\knjige_ločeno'
# ime datoteke s posameznimi knjigami
each_filename = 'knjiga{}.html'
# ime CSV datotek v katere bomo shranili podatke
csv_filenameV = 'knjige.csv'
csv_filenameK = 'knjiga.csv'
# regularni izraz, ki razbije knjige na posamezne dele
regex_each = re.compile(
    r'<div id="descriptionContainer">.*?'
    r'<span id="rating_graph"',
    re.DOTALL
)
# regularni izraz, ki vzame podatke o knjigi iz njene strani
regex_bd = re.compile(
    r'<meta content=\'https://www.goodreads.com/author/show/(?P<ID_avtorja>.*?)\.'
    r'.*?property=\'books:author\'>.*?'
    r'<div id="descriptionContainer">.*?'
    r'(?P<vsebina>.*?)</div>.*?'
    r'<div id="details" class="uitext darkGreyText">.*?'
    r'<div class="row">'
    r'(<span itemprop="bookFormat">|)(?P<vezava>[\w|\s]{0,30})(</span>|).*?'
    r'(<span itemprop="numberOfPages">|)(?P<stevilo_strani>\d*?)( pages?</span>|)</div>.*?'
    r'(<div class="row">|).*?(Published|Expected publication:).*?\s(?P<izdano>\d{0,4})\n.*?</div>.*?'
    ,
    re.DOTALL
)

def get_book_ids(directory, csv_IDs):
    path = os.path.join(directory, csv_IDs)
    ids = set()
    with open(path, "r", encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            ids.add(int(row["ID_knjige"]))
    ids = sorted(ids)
    return ids


def write_csv(fieldnames, rows, directory, csv_filename):
    """V csv_filename datoteko, ki jo nahaja directory, v podatke fieldnames zapiše pripadajoče podatke rows"""
    os.makedirs(directory, exist_ok=True)
    path = os.path.join(directory, csv_filename)
    with open(path, 'w', encoding='utf-8') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def purify_content(vsebina):
    """Počisti vsebino."""
    vsebina = vsebina.split('span id="freeText')
    besedilo = ''
    if not vsebina:
        return besedilo
    v_besedilu = False
    vsebina = vsebina[-1]
    for i in vsebina:
        if i == '\n':
            break
        elif i in "<>":
            v_besedilu = not v_besedilu
            continue
        if v_besedilu:
            besedilo += i
    return besedilo


def get_dict_from_single_block(directory, fp_filename, regex_d):
    """Vrne slovar ID_avtorja in avtorja"""
    path = os.path.join(directory, fp_filename)
    with open(path, "r", encoding='utf-8') as f:
        a = regex_d.search(f.read())
        a = a.groupdict()
        for item in a:
            a[item] = a[item].strip()
            if item == "vsebina":
                a[item] = purify_content(a[item])
        return a


def write_book_site_to_csv(directory_read, directory_write, each_filename, csv_IDs, csv_filename, regex_d):
    ids = get_book_ids(directory_write, csv_IDs)
    vrstice = []
    for ID in ids:
        print(ID)
        slovar = get_dict_from_single_block(directory_read, each_filename.format(ID), regex_d)
        vrstice.append(slovar)
    header = []
    for i in vrstice[0].keys():
        header.append(str(i))
    write_csv(header, vrstice, directory_write, csv_filename)




# ids = get_book_ids(directory, csv_filenameV)
# print(ids)
# print(len(ids))
#
# j = 1
# for i in ids[:]:
#     # if j != 1426 and j != 1451 and j != 1461 and j != 1908 and j != 2245 and j != 2417 and j != 2423 and j != 2586 \
#     #         and j != 2681 and j != 2740 and j != 2794 and j != 2820 and j != 2830:
#     print(j, i)
#     print(get_dict_from_single_block(directory_knjige, each_filename.format(i), regex_bd))
#     j += 1
