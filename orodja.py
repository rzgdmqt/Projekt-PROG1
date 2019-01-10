import requests
import re
import os
import csv
import sys


book_url = 'https://www.goodreads.com{}'
goodreads_frontpage_url = 'https://www.goodreads.com/list/show/6.Best_Books_of_the_20th_Century?page=1'
# mapa, v katero bomo shranili podatke
directory_write = r'html_strani_in_csv'
directory_books_html = r'html_strani_in_csv/knjige_ločeno' # popravi naslov
directory_authors_html = r'html_strani_in_csv/avtorji_ločeno' # popravi naslov
# ime datoteke v katero bomo shranili glavno stran
frontpage_filename = 'frontpage.html'
# ime datoteke s posameznimi knjigami
book_filename = 'knjiga{}.html'
# ime datoteke z avtorjevo stranjo
author_filename = 'autor{}.html'
# ime CSV datotek v katere bomo shranili podatke
csv_all = 'knjige_pomozna_vse.csv'
csv_each = 'knjige_pomozna_vsaka.csv'
csv_authors = 'avtorji.csv'
csv_books = 'knjige.csv'
# regularni izraz, ki razbije stran na posamezne knjige
regex_book_block = re.compile(
            r'<tr itemscope itemtype.*?Error rating book. Refresh and try again.',
            re.DOTALL
    )
# regularni izraz, ki razbije knjigo na posamezne podatke
regex_book_data_general = re.compile(
    r'<tr itemscope itemtype=.*?'
    r'<div id="(?P<ID_knjige>.*?)" class="u-anchorTarget"></div>.*?'
    r'<a title=".*?" href="(?P<url_knjige>.*?)">.*?'
    r"itemprop='name'>(?P<naslov>.*?)</span>.*?"
    r'itemprop="url" href="(?P<url_avtorja>https://www.goodreads.com/author/show/(?P<ID_avtorja>.*?)\..*?)">'
    r'<span itemprop="name">(?P<avtor>.*?)</span></a>.*?'
    r'</span> (?P<ocena>\d\.\d{2}) avg rating.*?'
    r'&mdash; (?P<koliko_ocen>.+?) ratings</span>.*?'
    r'<a href="#" onclick=.*?>score: (?P<tocke>.*?)</a>.*?'
    r'return false;">(?P<stevilo_glasov>.*?) people voted</a>',
    re.DOTALL
)
# regularni izraz, ki vzame podatke o knjigi iz njene strani
regex_book_data = re.compile(
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
regex_author_data = re.compile(
    r'href="https://www.goodreads.com/author/show/(?P<ID_avtorja>.*?)\.\w*?" />.*?'
    r'<div>.[\s\n]*?<h1 class="authorName">[\s\n]*?<span itemprop="name">(?P<avtor>.*?)'
    r'</span>[\s\n]*?</h1>[\s\n]*?.*?</div>'
    r'(<div class="dataTitle">Born</div>[\n\s]*?|)'
    r'(?P<kraj_rojstva>[\s\w,.]+?\n)([\n\s]*?|).*?'
    r'(<div class="dataTitle">Born</div>[\n\s]*?|)(?P<leto_rojstva>[\s\w,.]+?\n)([\n\s]*?|)[\n\s]'
    ,
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
    """Prenese num strani in jih shrani v isto datoteko."""
    url = url[:-1] + '{}'
    save_url_to_file(url.format(1), directory, fp_filename, "w", True)
    for i in range(2, num + 1):
        save_url_to_file(url.format(i), directory, fp_filename, "a", True)


def download_book_site():
    """Shrani stran knjige."""
    path = os.path.join(directory_write, csv_all)
    slovarji = []
    with open(path, "r", encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            slovarji.append(row)
    for i in slovarji:
        save_url_to_file(book_url.format(i["url_knjige"]), directory_books_html, book_filename.format(i["ID_knjige"]))


def download_author_page():
    """Shrani stran avtorja."""
    path = os.path.join(directory_write, csv_all)
    slovarji = []
    with open(path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            slovarji.append(row)
    for i in slovarji:
        save_url_to_file(i["url_avtorja"], directory_authors_html, author_filename.format(i["ID_avtorja"]))


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


def page_to_books():
    """Razdelimo stran na posamezne knjige."""
    path = os.path.join(directory_write, frontpage_filename)
    with open(path, "r", encoding='utf-8') as f:
        return [ujemanje.group(0) for ujemanje in regex_book_block.finditer(f.read())]


def get_dict_from_book_block():
    """Vrne seznam slovarjev z naslovom, avtorjem, oceno, številom ocen, točk, številom glasov in ID."""
    strani = page_to_books()
    slovarji = []
    for stran in strani:
        a = regex_book_data_general.search(stran).groupdict()
        for item in a:
            a[item] = a[item].strip()
        slovarji.append(a)
    return slovarji


def get_dict_from_single_block(directory, filename, regex_data):
    """Vrne slovar ključev in vrednosti."""
    path = os.path.join(directory, filename)
    with open(path, "r", encoding='utf-8') as f:
        a = regex_data.search(f.read())
        a = a.groupdict()
        for item in a:
            a[item] = a[item].strip()
            if item == "vsebina":
                a[item] = purify_content(a[item])
            if item == "leto_rojstva":
                a[item] = a[item].split(", ")[-1]
                if len(a[item]) > 4:
                    a[item] = '19' + a[item][-2:]
        return a


def get_authors_ids():
    """Vrne ID avtorjev, v naraščajočem v.r."""
    path = os.path.join(directory_write, csv_all)
    ids = set()
    with open(path, "r", encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            ids.add(int(row["ID_avtorja"]))
    ids = sorted(ids)
    return ids


def get_book_ids():
    """Vrne ID knjig, v naraščajočem v.r."""
    path = os.path.join(directory_write, csv_all)
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


def write_books_to_csv():
    """Knjige s splošne strani zapiše v csv."""
    slovarji = get_dict_from_book_block()
    header = []
    for i in slovarji[0].keys():
        header.append(str(i))
    write_csv(header, slovarji, directory_write, csv_all)


def write_authors_to_csv():
    """Zapiše avtorje v csv."""
    ids = get_authors_ids()
    vrstice = []
    for ID in ids:
        slovar = get_dict_from_single_block(directory_authors_html, author_filename.format(ID), regex_author_data)
        try:
            if slovar["kraj_rojstva"][:2] == "in":
                slovar["kraj_rojstva"] = slovar["kraj_rojstva"][3:]
        except:
            pass
        vrstice.append(slovar)
    header = []
    for i in vrstice[0].keys():
        header.append(str(i))
    write_csv(header, vrstice, directory_write, csv_authors)


def write_book_site_to_csv():
    """Zapiše knjige v csv"""
    ids = get_book_ids()
    vrstice = []
    for ID in ids:
        slovar = get_dict_from_single_block(directory_books_html, book_filename.format(ID), regex_book_data)
        slovar["ID_knjige"] = ID
        vrstice.append(slovar)
    header = []
    for i in vrstice[0].keys():
        header.append(str(i))
    write_csv(header, vrstice, directory_write, csv_each)


def merge_dicts(*dicts):
    result = {}
    for dictionary in dicts:
        result.update(dictionary)
    return result
