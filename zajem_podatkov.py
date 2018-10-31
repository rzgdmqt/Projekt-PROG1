import requests
import re
import os
import csv
import sys


book_url = 'https://www.goodreads.com{}'
goodreads_frontpage_url = 'https://www.goodreads.com/list/show/6.Best_Books_of_the_20th_Century?page=1'
# mapa, v katero bomo shranili podatke
directory = r'C:\Users\MasterX\Desktop\UVP\Projekt-PROG1\html_strani_in_csv'
directory_knjige = r'C:\Users\MasterX\Desktop\UVP\Projekt-PROG1\html_strani_in_csv\knjige_ločeno'
directory_avtorji = r'C:\Users\MasterX\Desktop\UVP\Projekt-PROG1\html_strani_in_csv\avtorji_ločeno'
# ime datoteke v katero bomo shranili glavno stran
frontpage_filename = 'frontpage.html'
# ime datoteke s posameznimi knjigami
each_filename = 'knjiga{}.html'
# ime datoteke z avtorjevo stranjo
author_filename = 'autor{}.html'
# ime CSV datotek v katere bomo shranili podatke
csv_filenameV = 'knjige.csv'
csv_filenameK = 'knjiga.csv'
csv_filenameA = 'avtor.csv'
# regularni izraz, ki razbije stran na posamezne knjige
regex_books = re.compile(
            r'<tr itemscope itemtype.*?Error rating book. Refresh and try again.',
            re.DOTALL
    )
# regularni izraz, ki razbije knjigo na posamezne podatke
regex_data = re.compile(
    r'<tr itemscope itemtype=.*?'
    r'<div id="(?P<ID_knjige>.*?)" class="u-anchorTarget"></div>.*?'
    r'<a title=".*?" href="(?P<url_knjige>.*?)">.*?'
    r"itemprop='name'>(?P<naslov>.*?)</span>.*?"
    r'itemprop="url" href="(?P<url_avtorja>https://www.goodreads.com/author/show/(?P<ID_avtorja>.*?)\..*?)">'
    r'<span itemprop="name">(?P<avtor>.*?)</span></a>.*?'
    r'</span> (?P<ocena>.+?) avg rating.*?'
    r'&mdash; (?P<koliko_ocen>.+?) ratings</span>.*?'
    r'<a href="#" onclick=.*?>score: (?P<tocke>.*?)</a>.*?'
    r'return false;">(?P<stevilo_glasov>.*?) people voted</a>',
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
# regularni izraz, ki vzame podatke o avtorju
regex_ad = re.compile(
    r'href="https://www.goodreads.com/author/show/(?P<ID_avtorja>.*?)\.(?P<avtor>.*?)" />.*?',
    re.DOTALL
)


def save_url_to_file(url, directory, fp_filename, over_write="w", vsili_prenos=False):
    """Naloži URL in vsebino zapiše v datoteko."""
    try:
        print('Shranjujem {} ...'.format(url), end='')
        sys.stdout.flush()
        path = os.path.join(directory, fp_filename)
        if os.path.exists(path) and not vsili_prenos:
            print(" Shranjeno od prej.")
            return
        r = requests.get(url)
        print(" Shranjeno.")
    except requests.exceptions.ConnectionError:
        print("Ni dostopa " + url)
        return
    os.makedirs(directory, exist_ok=True)
    path = os.path.join(directory, fp_filename)
    with open(path, over_write, encoding='utf-8') as f:
        f.write(r.text)


def download_more_pages(num, url, directory, fp_filename):
    url = url[:-1] + '{}'
    save_url_to_file(url.format(1), directory, fp_filename)
    for i in range(2, num + 1):
        save_url_to_file(url.format(i), directory, fp_filename, "a", True)


def download_book_site(csv_filename, directory_read, directory_write, each_filename, book_url):
    path = os.path.join(directory_read, csv_filename)
    slovarji = []
    with open(path, "r", encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            slovarji.append(row)
    for i in slovarji:
        save_url_to_file(book_url.format(i["url_knjige"]), directory_write, each_filename.format(i["ID_knjige"]))


def download_author_page(csv_filename, directory_read, directory_write, author_filename):
    path = os.path.join(directory_read, csv_filename)
    slovarji = []
    with open(path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            slovarji.append(row)
    for i in slovarji:
        save_url_to_file(i["url_avtorja"], directory_write, author_filename.format(i["ID_avtorja"]))


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


def page_to_books(directory, fp_filename, regex_b):
    """Razdelimo stran na posamezne knjige."""
    path = os.path.join(directory, fp_filename)
    with open(path, "r", encoding='utf-8') as f:
        return [ujemanje.group(0) for ujemanje in regex_b.finditer(f.read())]


def get_dict_from_book_block(directory, fp_filename, regex_b, regex_d):
    """Vrne seznam slovarjev z naslovom, avtorjem, oceno, številom ocen, točk, številom glasov in ID."""
    strani = page_to_books(directory, fp_filename, regex_b)
    slovarji = []

    for stran in strani:
        a = regex_d.search(stran).groupdict()
        for item in a:
            a[item] = a[item].strip()
        slovarji.append(a)
    return slovarji


def get_dict_from_single_block(directory, fp_filename, regex_d):
    """Vrne slovar ključev in vrednosti."""
    path = os.path.join(directory, fp_filename)
    with open(path, "r", encoding='utf-8') as f:
        a = regex_d.search(f.read())
        a = a.groupdict()
        for item in a:
            a[item] = a[item].strip()
            if item == "vsebina":
                a[item] = purify_content(a[item])
            elif item == "avtor":
                avtor = ''
                for i in a[item].split('_'):
                    if len(i) == 1:
                        avtor += i + '. '
                    else:
                        avtor += i + ' '
                a[item] = avtor.strip()
        return a


def get_authors_ids(directory, csv_IDs):
    path = os.path.join(directory, csv_IDs)
    ids = set()
    with open(path, "r", encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            ids.add(int(row["ID_avtorja"]))
    ids = sorted(ids)
    return ids


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


def write_books_to_csv(directory, fp_filename, csv_filename, regex_b, regex_d):
    slovarji = get_dict_from_book_block(directory, fp_filename, regex_b, regex_d)
    header = []
    for i in slovarji[0].keys():
        header.append(str(i))
    write_csv(header, slovarji, directory, csv_filename)


def write_authors_to_csv(directory_read, directory_write, author_filename, csv_IDs, csv_filename, regex_d):
    ids = get_authors_ids(directory_write, csv_IDs)
    vrstice = []
    for ID in ids:
        print(ID)
        slovar = get_dict_from_single_block(directory_read, author_filename.format(ID), regex_d)
        vrstice.append(slovar)
    header = []
    for i in vrstice[0].keys():
        header.append(str(i))
    write_csv(header, vrstice, directory_write, csv_filename)


def write_book_site_to_csv(directory_read, directory_write, each_filename, csv_IDs, csv_filename, regex_d):
    ids = get_book_ids(directory_write, csv_IDs)
    vrstice = []
    for ID in ids:
        slovar = get_dict_from_single_block(directory_read, each_filename.format(ID), regex_d)
        vrstice.append(slovar)
    header = []
    for i in vrstice[0].keys():
        header.append(str(i))
    write_csv(header, vrstice, directory_write, csv_filename)


write_authors_to_csv(directory_avtorji, directory, author_filename, csv_filenameV, csv_filenameA, regex_ad)
