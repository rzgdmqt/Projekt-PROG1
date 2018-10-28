import requests
import re
import os
import csv
import sys


book_url = "https://www.goodreads.com/book/show/{}"
goodreads_frontpage_url = 'https://www.goodreads.com/list/show/6.Best_Books_of_the_20th_Century?page=1'
# mapa, v katero bomo shranili podatke
directory = r'C:\Users\MasterX\Desktop\UVP\Projekt-PROG1\html_strani_in_csv'
# ime datoteke v katero bomo shranili glavno stran
frontpage_filename = 'frontpage.html'
# ime CSV datoteke v katero bomo shranili podatke
csv_filename = 'knjige.csv'
# ime datoteke s posameznimi knjigami
each_filename = 'each.html'
# regularni izraz, ki razbije stran na posamezne knjige
regex_books = re.compile(
            r'<tr itemscope itemtype.*?Error rating book. Refresh and try again.',
            re.DOTALL
    )
# regularni izraz, ki razbije knjigo na posamezne podatke
regex_data = re.compile(
    r'<tr itemscope itemtype=.*?'
    r'<div id="(?P<ID>.*?)" class="u-anchorTarget"></div>.*?'
    r"itemprop='name'>(?P<naslov>.*?)</span>.*?"
    r'<span itemprop="name">(?P<avtor>.*?)</span></a>.*?'
    r'</span> (?P<ocena>.+?) avg rating.*?'
    r'&mdash; (?P<koliko_ocen>.+?) ratings</span>.*?'
    r'<a href="#" onclick=.*?>score: (?P<tocke>.*?)</a>.*?'
    r'return false;">(?P<stevilo_glasov>.*?) people voted</a>',
    re.DOTALL
)
regex_each = re.compile(
    r'<title>.*?</title>.*?',
    re.DOTALL
)



def save_url_to_file(url, directory, fp_filename, over_write="w"):
    """Naloži URL in vsebino zapiše v datoteko."""
    try:
        print('Shranjujem {} ...'.format(url), end='')
        sys.stdout.flush()
        if os.path.isfile(fp_filename):
            print("Shranjeno od prej.")
            return
        r = requests.get(url)
        print("Shranjeno.")
    except requests.exceptions.ConnectionError:
        print("Ni dostopa " + url)
        return
    os.makedirs(directory, exist_ok=True)
    path = os.path.join(directory, fp_filename)
    with open(path, over_write, encoding='utf-8') as f:
        f.write(r.text)


def page_to_books(directory, fp_filename, regex_b):
    """Razdelimo stran na posamezne knjige."""
    with open(os.path.join(directory, fp_filename), "r") as f:
        return [ujemanje.group(0) for ujemanje in regex_b.finditer(f.read())]


def get_dict_from_book_block(directory, fp_filename, regex_b, regex_d):
    """Vrne seznam slovarjev z naslovom, avtorjem, oceno, številom ocen, točk, številom glasov in ID."""
    strani = page_to_books(directory, fp_filename, regex_b)
    slovarji = []

    for stran in strani:
        a = regex_d.search(stran).groupdict()
        for item in a:
            a[item] = a[item].replace(",", ".").strip()
        slovarji.append(a)
    return slovarji


def write_csv(fieldnames, rows, directory, csv_filename):
    """V csv_filename datoteko, ki se nahaja v directory v podatke dieldnames zapiše pripadajoče podatke rows"""
    os.makedirs(directory, exist_ok=True)
    path = os.path.join(directory, csv_filename)
    with open(path, 'w') as csv_file:
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
        save_url_to_file(url.format(i), directory, fp_filename, "a")


def download_book_site(page_url, directory, csv_filename, each_filename):
    path = os.path.join(directory, csv_filename)
    ids = []
    with open(path, "r") as f:
        for line in f:
            ids.append(line.split(",")[0])
    print(ids)
    for ID in ids[1:]:
        if ID != "\n":
            save_url_to_file(page_url.format(ID), directory, each_filename, "a")

