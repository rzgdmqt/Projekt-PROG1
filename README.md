# Analiza najbolj branih knjig 20. stol.

Pri predmetu Programiranje 1 moram pripraviti projektno nalogo iz analize podatkov. Odločil sem se, da si podatke pridobim s strani [Goodreads](https://www.goodreads.com/list/show/6.Best_Books_of_the_20th_Century?page=1) z uporabo pythona, nato pa jih bom analiziral. Omejil se bom na najboljše knjige dvajsetega stoletja, ki so po mnenju bralcev najboljša.

Za vsako knjigo sem zajel:
- knjige.csv vsebuje:
  - ID knjige
  - ID avtorja
  - naslov knjige
  - stevilo strani
  - vsebina
  - oceno
  - vezavo
  - leto izida
- avtorji.csv vsebuje:
  - avtorja (ID, kraj in leto rojstva)
ostali pomožni csv datoteki služita zgolj lažjemu shranjevanju strani in sta združeni v datoteki knjige.csv (brez hiper povezave do avtorja in knjige same.)


Delovne hipoteze:
- Knjige katerega avtorja so najboljše?
- Kateri žanri so najbolj priljubljeni?
- Kakšna je povprečna ocena knjig?
- Kakšen je "score" v primerjavi s povprečno oceno?
- Ali dolžina predstavitve knjige vpliva na oceno?
- Po navdihu še kaj.
