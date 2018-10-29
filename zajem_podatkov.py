import requests
import re
import os
import csv
import sys


author_url = 'https://www.goodreads.com/author/show/{}'
book_url = 'https://www.goodreads.com/book/show/{}'
goodreads_frontpage_url = 'https://www.goodreads.com/list/show/6.Best_Books_of_the_20th_Century?page=1'
# mapa, v katero bomo shranili podatke
directory = r'C:\Users\MasterX\Desktop\UVP\Projekt-PROG1\html_strani_in_csv'
# ime datoteke v katero bomo shranili glavno stran
frontpage_filename = 'frontpage.html'
# ime datoteke s posameznimi knjigami
each_filename = 'each.html'
# ime datoteke z avtorjevo stranjo
author_filename = 'author.html'
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
    r"itemprop='name'>(?P<naslov>.*?)</span>.*?"
    r'<span itemprop="name">(?P<avtor>.*?)</span></a>.*?'
    r'</span> (?P<ocena>.+?) avg rating.*?'
    r'&mdash; (?P<koliko_ocen>.+?) ratings</span>.*?'
    r'<a href="#" onclick=.*?>score: (?P<tocke>.*?)</a>.*?'
    r'return false;">(?P<stevilo_glasov>.*?) people voted</a>',
    re.DOTALL
)
# regularni izraz, ki razbije knjige na posamezne dele
regex_each = re.compile(
    r'<div id="descriptionContainer">.*?'
    r'<span id="rating_graph"',
    re.DOTALL
)
# regularni izraz, ki vzame podatke o knjigi iz njene strani
regex_bd = re.compile(
    r'<span id=".*?" style="display:none">(?P<vsebina>.*?)</span>.*?'
    r'<span itemprop="bookFormat">(?P<vezava>.*?)</span>.*?'
    r'"numberOfPages">(?P<stevilo_strani>.*?) pages?</span>.*?'
    r'Published(?P<izdano>.*?)by.*?'
    r'<div class="infoBoxRowItem" itemprop=.*?>(?P<jezik>.*?)</div>.*?'
    r'<a href="/author/list/(?P<ID_avtorja>.*?)\..*?</a>',
    re.DOTALL
)
# regularni izraz, ki razbije avtorje na posamezne dele
regex_a = re.compile(
    r'<head>.*?'
    r'</html>'
)
# regularni izraz, ki vzame podatke o avtorju
regex_ad = re.compile(
    r'<a data-text-id="author(?P<ID_avtorja>.*?)" href='
    r'<div class="dataItem" itemprop=.*?>.*?\s*(?P<rojstvo>.*?).*?</div>',
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


def page_to_books(directory, fp_filename, regex_b):
    """Razdelimo stran na posamezne knjige."""
    with open(os.path.join(directory, fp_filename), "r", encoding='utf-8') as f:
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


def download_more_pages(num, url, directory, fp_filename):
    url = url[:-1] + '{}'
    save_url_to_file(url.format(1), directory, fp_filename)
    for i in range(2, num + 1):
        save_url_to_file(url.format(i), directory, fp_filename, "a", True)


def download_book_site(page_url, directory, csv_filename, each_filename):
    path = os.path.join(directory, csv_filename)
    ids = []
    with open(path, "r", encoding='utf-8') as f:
        for line in f:
            if "ID" in line.split(",")[0]:
                ids.append(line.split(",")[0])
            else:
                ids.append(line.split(",")[-1])
    for ID in ids[1:]:
        if ID != "\n":
            save_url_to_file(page_url.format(ID), directory, each_filename, "a", True)

