"""
Pythonilla toteutettu versio miinaharava pelistä.
Tekijä: Julius Välimaa, julius.valimaa@gmail.com
"""
from copy import deepcopy
import datetime
import random

import haravasto

VAIKEUSASTEET = {
    "helppo": {"ruutuja": 10, "miinoja": 10, "piirtomarginaali": 300},
    "normaali": {"ruutuja": 15, "miinoja": 38, "piirtomarginaali": 200},
    "vaikea": {"ruutuja": 20, "miinoja": 60, "piirtomarginaali": 100}
}

MERKIT = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "f", "x"]

tila = {
    "kentta": [],
    "naytto": [],
    "vaikeus": {},
    "nimi": None,
    "aika": "00:00:00",
    "ajasta": False,
    "aloitus": None,
    "nyt": None,
    "vuoro": None,
    "jaljella": None,
    "havio": False,
    "voitto": False,
    "loppu": False,
}
piirto = {
    "ruudukko": [],
    "kuva": 0,
    "nopeus": 0.02,
    "toistot": 520
}


def nayta_paavalikko():
    """
    Esittää päävalikon terminaalissa.
    """
    try:
        while True:
            print("Tervetuloa Python miinaharavaan!")
            print("(A)loita uusi peli")
            print("(T)ulosta tilastot")
            print("(L)opeta")
            syote = input(
                "Valitse haluttu toiminto syöttämällä korostettu näppäin: ")
            syote = syote.strip().lower()
            if syote == "a":
                aloita_peli()
            elif syote == "t":
                tulosta_tilastot()
            elif syote == "l":
                print("Hei hei!")
                break
            else:
                print("Anna oikea syöte! (a, t, l)")
    except (KeyboardInterrupt, EOFError):
        print()
        print("Hei hei!")


def luo_tilastot():
    """
    Luo tilastoihin tallennettavan rivin päättyneen pelin tiedoilla.
    """
    if tila["voitto"]:
        lopputulos = "Voitto"
    elif tila["havio"]:
        lopputulos = "Häviö"
    paivays = datetime.datetime.isoformat(
        datetime.datetime.now(), sep=" ", timespec="seconds")
    tiedot = ("{nimi},{aika},{vuoro},{miinoja},{koko},{tulos},"
        "{paivays}\n").format(
            nimi=tila["nimi"],
            aika=tila["aika"],
            vuoro=tila["vuoro"],
            miinoja=tila["vaikeus"]["miinoja"],
            koko=tila["vaikeus"]["ruutuja"],
            tulos=lopputulos,
            paivays=paivays
        )
    return tiedot


def tulosta_tilastot():
    """
    Tulostaa tilastot terminaaliin.
    """
    try:
        with open("tilastot.CSV", "r") as tilastot:
            tiedot = []
            for rivi in tilastot.readlines():
                tiedot.append(rivi.strip())
            tulostuksia = int((len(tiedot) / 5 + 0.95))
            print("nimi aika vuoro miinoja leveysxkorkeus tulos paivays")
            for i in range(tulostuksia):
                alku = i * 5
                loppu = (i + 1) * 5
                muotoile_tulostus(tiedot[alku:loppu])
                if i < tulostuksia - 1:
                    input("--paina ENTER jatkaaksesi tulostusta--")
            print()
    except OSError:
        print("Tilasto tiedostoa ei löytynyt")


def muotoile_tulostus(sivu):
    """
    Muotoilee sivun ja tulostaa sen.
    """
    for rivi in sivu:
        nimi, aika, vuoro, miinat, koko, tulos, paivays = rivi.split(",")
        print(("{nimi} {aika} {vuoro} {miinoja} {koko}x{koko} {tulos} "
            "{paivays}").format(
                nimi=nimi,
                aika=aika,
                vuoro=vuoro,
                miinoja=miinat,
                koko=koko,
                tulos=tulos,
                paivays=paivays
            ))


def tallenna_tilastot():
    """
    Tallentaa päättyneen pelin tiedot tilastoihin:
    """
    if tila["voitto"] or tila["havio"]:
        try:
            with open("tilastot.CSV", "a") as tilastot:
                tilastot.write(luo_tilastot())
        except OSError:
            print("Tilasto tiedostoa ei löytynyt")


def aloita_peli():
    """
    Aloittaa uuden pelin. Tallentaa tilastot ja nollaa sanakirjat,
    kun peli loppuu.
    """
    while True:
        nimi = input("Anna käyttäjänimi(max 8 merkkiä): ").strip()
        if len(nimi) > 8:
            print("Nimi on liian pitkä")
        elif "," in nimi:
            print("Pilkku ei ole sallittu")
        else:
            tila["nimi"] = nimi
            break
    print("Valitse vaikeusaste:")
    print("(H)elppo")
    print("(N)ormaali")
    print("(V)aikea")
    while True:
        syote = input("Valinta: ").strip().lower()
        if syote == "h":
            tila["vaikeus"] = VAIKEUSASTEET["helppo"]
            break
        elif syote == "n":
            tila["vaikeus"] = VAIKEUSASTEET["normaali"]
            break
        elif syote == "v":
            tila["vaikeus"] = VAIKEUSASTEET["vaikea"]
            break
        else:
            print("Anna oikea syöte!(h, n, v)")
    print("Ohjeet: Klikkaa hiiren vasemmalla näppäimellä ruutua,")
    print("jonka haluat avata. Klikkaa oikealla asettaaksesi lipun.")
    print("Peli päätty, kun osut miinaan tai kentällä ei ole ruutuja,")
    print("joissa ei ole lippua.")
    input("--Paina ENTER aloittaaksesi pelin--")
    luo_kentta()
    haravasto.lataa_kuvat("spritet")
    haravasto.luo_ikkuna(
        leveys=1000, korkeus=1000)
    haravasto.aseta_piirto_kasittelija(piirra_kentta)
    haravasto.aseta_hiiri_kasittelija(kasittele_hiiri)
    haravasto.aseta_toistuva_kasittelija(paivita_peli)
    haravasto.aloita()
    tallenna_tilastot()
    nollaa_sanakirjat()


def nollaa_sanakirjat():
    """
    Palauttaa pelin aikana tilan tarkasteluun käytetyt sanakirjat
    alkuperäiseen tilaansa.
    """
    tila["kentta"] = []
    tila["naytto"] = []
    tila["vaikeus"] = {}
    tila["nimi"] = None
    tila["aika"] = "00:00:00"
    tila["ajasta"] = False
    tila["aloitus"] = None
    tila["nyt"] = None
    tila["vuoro"] = None
    tila["jaljella"] = None
    tila["havio"] = False
    tila["voitto"] = False
    tila["loppu"] = False
    piirto["ruudukko"] = []
    piirto["kuva"] = 0
    piirto["toistot"] = 520


def luo_kentta():
    """
    Funktio joka luo valitun vaikeusasteen pohjalta miinakentän.
    """
    koko = tila["vaikeus"]["ruutuja"]
    for rivi in range(koko):
        tila["kentta"].append([])
        for sarake in range(koko):
            tila["kentta"][-1].append(" ")
    tila["naytto"] = deepcopy(tila["kentta"])


def maarita_ymparoivat(kentta, x_koordinaatti, y_koordinaatti):
    """
    Funktio määrittää annettua ruutua ympäröivät 8 ruutua ja tarkistaa
    ovatko ne kentän sisällä. Palauttaa sisällä olevat ruudut (x, y)
    -koordinaatti pareina listassa.
    """
    rajat = {
        "leveys_min": 0,
        "leveys_max": len(kentta[0]) - 1,
        "korkeus_min": 0,
        "korkeus_max": len(kentta) - 1
    }
    tarkistetut = []
    rivit = [y_koordinaatti - 1, y_koordinaatti, y_koordinaatti + 1]
    sarakkeet = [x_koordinaatti - 1, x_koordinaatti, x_koordinaatti + 1]
    for rivi in rivit:
        for sarake in sarakkeet:
            if ((rajat["korkeus_min"] <= rivi <= rajat["korkeus_max"]) and
                (rajat["leveys_min"] <= sarake <= rajat["leveys_max"])):
                # Ehtojen täyttyessä
                tarkistetut.append((sarake, rivi))
    return tarkistetut


def miinoita(kentta, x_alku, y_alku):
    """
    Asettaa kentälle N kpl miinoja satunaisiin paikkoihin.
    """
    n_miinoja = tila["vaikeus"]["miinoja"]
    tila["jaljella"] = n_miinoja
    vapaat_rudut = []
    for x in range(len(kentta)):
        for y in range(len(kentta)):
            vapaat_rudut.append((x, y))
    turva_alue = maarita_ymparoivat(kentta, x_alku, y_alku)
    for x, y in turva_alue:
        vapaat_rudut.remove((x, y))
    while n_miinoja > 0:
        x, y = random.choice(vapaat_rudut)
        vapaat_rudut.remove((x, y))
        kentta[y][x] = "x"
        n_miinoja -= 1
    for y, rivi in enumerate(kentta):
        for x, merkki in enumerate(rivi):
            if merkki == " ":
                kentta[y][x] = str(laske_miinat(kentta, x, y))


def laske_miinat(ruudukko, x_koordinaatti, y_koordinaatti):
    """
    Laskee annetulle kentän ruudulle, montako miinaa sen ympärillä on.
    """
    kasittely = maarita_ymparoivat(ruudukko, x_koordinaatti, y_koordinaatti)
    miinoja = 0
    for x, y in kasittely:
        merkki = ruudukko[y][x]
        if merkki == "x":
            miinoja += 1
    return miinoja


def tarkista_voitto():
    """
    Tarkistaa onko voittoehto täyttynyt.
    """
    ei_tyhja = 0
    for rivi in tila["naytto"]:
        for merkki in rivi:
            if merkki in MERKIT:
                ei_tyhja += 1
    if ei_tyhja == (len(tila["naytto"]) * len(tila["naytto"][0])):
        tila["voitto"] = True


def paivita_peli(kulunut_aika):
    """
    Päivitää pelin tilannetta. Tarkastelee voito ja häviö ehtoja ja toteuttaa
    tarvittavat toimet niiden täyttyessä. Päivittää kelloa.
    """
    piirto["ruudukko"] = tila["naytto"]
    if tila["jaljella"] == 0:
        tarkista_voitto()
    if tila["havio"] or tila["voitto"]:
        if tila["ajasta"]:
            tila["ajasta"] = False
        if piirto["toistot"] > 0:
            animaatio = [tila["kentta"], tila["naytto"]]
            piirto["ruudukko"] = animaatio[int(piirto["kuva"] % 2)]
            piirto["kuva"] += piirto["nopeus"]
            piirto["toistot"] -= 1
        else:
            tila["loppu"] = True
        if tila["loppu"]:
            haravasto.lopeta()
    if tila["ajasta"]:
        tila["nyt"] = datetime.datetime.now()
        try:
            aika, millit = str(tila["nyt"] - tila["aloitus"]).split(".")
        except ValueError:
            aika = str(tila["nyt"] - tila["aloitus"])
        tila["aika"] = aika


def kasittele_hiiri(hiiri_x, hiiri_y, hiiri_nappain, muokkaus_nappaimet):
    """
    Tätä funktiota kutsutaan, kun käyttäjä klikkaa sovellusikkunaan
    hiirellä. Ensimmäinen klikkaus kentän sisään luo miinakentän ja
    peli alkaa. Vasen klikkaus avaa ruudun ja, jos ruutu ei ole numero,
    aloittaa tulvatäytön kyseisestä ruudusta. Jos ruudussa on miina,
    käynnistää häviö prosessin. Oikea klikkaus asettaa ruutuun lipun
    ja poistaa sen, jos ruudussa on jo lippu.
    """
    hiiren_nappaimet = {
        "vasen": haravasto.HIIRI_VASEN,
        "keski": haravasto.HIIRI_KESKI,
        "oikea": haravasto.HIIRI_OIKEA
    }
    rajat = {
        "leveys_min": 0,
        "leveys_max": len(tila["kentta"][0]) - 1,
        "korkeus_min": 0,
        "korkeus_max": len(tila["kentta"]) - 1
    }
    x = ((hiiri_x - tila["vaikeus"]["piirtomarginaali"]) // 40)
    y = ((hiiri_y - tila["vaikeus"]["piirtomarginaali"]) // 40)
    if ((rajat["korkeus_min"] <= y <= rajat["korkeus_max"]) and
        (rajat["leveys_min"] <= x <= rajat["leveys_max"])):
        # Ehtojen täyttyessä
        if tila["vuoro"] is None:
            miinoita(tila["kentta"], x, y)
            tila["vuoro"] = 0
            tila["aloitus"] = datetime.datetime.now()
            tila["ajasta"] = True
        if hiiri_nappain == hiiren_nappaimet["vasen"]:
            if tila["kentta"][y][x] == "x" and tila["naytto"][y][x] != "f":
                tila["havio"] = True
            elif (tila["kentta"][y][x] in MERKIT[1:-2] and
                tila["naytto"][y][x] == " "):
                # Ehtojen täyttyessä
                tila["naytto"][y][x] = tila["kentta"][y][x]
                tila["vuoro"] += 1
            elif tila["naytto"][y][x] == " " and tila["naytto"][y][x] != "f":
                tulvataytto(x, y)
                tila["vuoro"] += 1
        elif hiiri_nappain == hiiren_nappaimet["oikea"]:
            if tila["naytto"][y][x] == " " and tila["jaljella"] > 0:
                tila["naytto"][y][x] = "f"
                tila["jaljella"] -= 1
            elif tila["naytto"][y][x] == "f":
                tila["naytto"][y][x] = " "
                tila["jaljella"] += 1


def tulvataytto(x_alku, y_alku):
    """
    Muuttaa näytettävällä kentällä olevat tuntemattomat ruudut
    loogista kenttää vastaavaksi siten, että täyttö aloitetaan
    annetusta x, y -pisteestä.
    """
    tuntemattomat = [
        (x_alku, y_alku),
    ]
    while tuntemattomat:
        x_kasit, y_kasit = tuntemattomat.pop()
        tila["naytto"][y_kasit][x_kasit] = tila["kentta"][y_kasit][x_kasit]
        kasiteltavat = maarita_ymparoivat(tila["naytto"], x_kasit, y_kasit)
        for x, y in kasiteltavat:
            if (tila["naytto"][y][x] == " " and
                tila["kentta"][y][x] in MERKIT[1:-2]):
                # Ehtojen täyttyessä
                tila["naytto"][y][x] = tila["kentta"][y][x]
                continue
            elif tila["naytto"][y][x] == " " and tila["kentta"][y][x] != "x":
                tuntemattomat.append((x, y))


def piirra_kentta():
    """
    Käsittelijäfunktio, joka piirtää kaksiulotteisena listana kuvatun
    miinakentän ruudut, kellon, vuoro ja miina laskurin näkyviin
    peli-ikkunaan. Funktiota kutsutaan aina kun pelimoottori pyytää
    ruudun näkymän päivitystä.
    """
    haravasto.tyhjaa_ikkuna()
    haravasto.piirra_tausta()
    haravasto.piirra_tekstia("Aika:", 50, 950)
    haravasto.piirra_tekstia(tila["aika"], 50, 910)
    haravasto.piirra_tekstia("Vuoro:", 800, 950)
    haravasto.piirra_tekstia(str(tila["vuoro"]), 800, 910)
    haravasto.piirra_tekstia("Miinoja jäljellä:", 350, 950)
    haravasto.piirra_tekstia(str(tila["jaljella"]), 350, 910)
    haravasto.aloita_ruutujen_piirto()
    for y, rivi in enumerate(piirto["ruudukko"]):
        for x, merkki in enumerate(rivi):
            haravasto.lisaa_piirrettava_ruutu(
                merkki,
                x * 40 + tila["vaikeus"]["piirtomarginaali"],
                y * 40 + tila["vaikeus"]["piirtomarginaali"]
            )
    haravasto.piirra_ruudut()


if __name__ == "__main__":
    nayta_paavalikko()
