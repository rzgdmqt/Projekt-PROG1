import requests
import re
import os
import csv
import sys


goodreads_frontpage_url = 'https://www.goodreads.com/list/show/6.Best_Books_of_the_20th_Century?page=1'
# mapa, v katero bomo shranili podatke
directory = r'C:\Users\MasterX\Desktop\UVP\Projekt-PROG1\html_strani'
# ime datoteke v katero bomo shranili glavno stran
frontpage_filename = 'frontpage.html'
# ime CSV datoteke v katero bomo shranili podatke
csv_filename = 'knjige.csv'


def save_url_to_file(url, directory, fp_filename):
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
    with open(path, 'w', encoding='utf-8') as f:
        f.write(r.text)


def page_to_books(directory, fp_filename):
    """Razdelimo stran na posamezne knjige."""
    regex = re.compile(
            r'<tr itemscope itemtype.*?Error rating book. Refresh and try again.',
            re.DOTALL
    )
    with open(os.path.join(directory, fp_filename), "r") as f:
        return [ujemanje.group(0) for ujemanje in regex.finditer(f.read())]


def get_dict_from_book_block(directory, fp_filename):
    """Vrne seznam slovarjev z naslovom, avtorjem, oceno, številom ocen, točk, številom glasov in ID."""
    regex = re.compile(
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
    strani = page_to_books(directory, fp_filename)
    slovarji = []

    for stran in strani:
        a = regex.search(stran).groupdict()
        a["ID"] = abs(int(a["ID"].strip()))
        a["naslov"] = str(a["naslov"].strip())
        a["avtor"] = str(a["avtor"].strip())
        a["ocena"] = abs(float(a["ocena"].strip()))
        a["koliko_ocen"] = abs(int(a["koliko_ocen"].strip().replace(",", "")))
        a["tocke"] = abs(int(a["tocke"].strip().replace(",", "")))
        a["stevilo_glasov"] = abs(int(a["stevilo_glasov"].strip().replace(",", "")))
        slovarji.append(a)
    return slovarji


def write_csv(fieldnames, rows, directory, csv_filename):
    """Naredi CSV file"""
    os.makedirs(directory, exist_ok=True)
    path = os.path.join(directory, csv_filename)
    with open(path, 'w') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def write_books_to_csv(directory, filename, csv_filename):
    slovarji = get_dict_from_book_block(directory, filename)
    header = []
    for i in slovarji[0].keys():
        header.append(str(i))
    write_csv(header, slovarji, directory, csv_filename)


def download_more_pages(num, url, directory, filename):
    url = url[:-1] + '{}'
    for i in range(1, num + 1):
        save_url_to_file(url, directory, filename)
