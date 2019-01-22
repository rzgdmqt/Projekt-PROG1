# Analiza najbolj branih knjig 20. stol.

Pri predmetu Programiranje 1 sem moral pripraviti projektno nalogo iz analize podatkov. Odločil sem se, da si podatke pridobim s strani [Goodreads](https://www.goodreads.com/list/show/6.Best_Books_of_the_20th_Century?page=1) z uporabo Pythona, nato pa sem jih analiziral. Omejil sem se na najboljše knjige dvajsetega stoletja, ki so po mnenju bralcev najboljše.

Za vsako knjigo sem zajel:
- knjige.csv vsebuje:
  - ID knjige
  - ID avtorja
  - naslov knjige
  - število strani
  - vsebino
  - oceno
  - število ocen
  - točke
  - število točk
  - vezavo
  - leto izida
- avtorji.csv vsebuje:
  - ID avtorja
  - kraj rojstva
  - leto rojstva

Delovne hipoteze:
- Knjige katerega avtorja so najboljše?
- Kakšna je povprečna ocena knjig?
- Kakšne so točke v primerjavi s povprečno oceno?
- Ali dolžina predstavitve knjige vpliva na oceno?
- Kakšna vezava knjig je najpogostejša dandanes?
- Ali je kakšna izmed najbolj branih knjig slovenska?

V datoteki 'orodja.py', se nahaja praktično vse, kar sem potreboval za zajem podatkov (funkcije, regularni izrazi, ciljne mape za shranjevanje datotek in posamezni spletni naslovi, iz katerih sem zajemal podatke). V datoteki zajem_podatkov.py pa se nahaja koda, ki sem jo pognal, da sem zajel podatke in si pripravil csv datoteke. Program v tej datoteki je napisan tako, da ga dejansko le poženeš, napišeš koliko podatkov želiš analizirati, ostalo pa se stori samo. Mape za shranjevanje so podane z relativnimi naslovi, tako da lahko ta program uporablja vsakkdo (če mapa še ne obstaja, se ustvari sama).

Za pregled analize podatkov, si ne rabiš pripravljati ničesar (če si kloniral repozitorij), saj so csv datoteke že pripravljene za uporabo, tako da vse kar moraš storiti je, da odpreš analiza_podatkov.ipynb in kar takoj preveriš nekaj (upam) zanimivih izsledkov. Obilo užitka pri branju.
