"""
Pythonilla toteutettu versio miinaharava pelistä.
Tekijä: Julius Välimaa, julius.valimaa@gmail.com
"""
import random
import datetime
import copy

import haravasto

VAIKEUSASTEET = {
    "helppo": {"ruutuja": 10, "miinoja": 10, "piirtomarginaali": 300},
    "normaali": {"ruutuja": 15, "miinoja": 22, "piirtomarginaali": 200},
    "vaikea": {"ruutuja": 20, "miinoja": 40, "piirtomarginaali": 100}
}

MERKIT = ["1", "2", "3", "4", "5", "6", "7", "8"]

tila = {
    "kentta": [],
    "naytto": [],
    "vaikeus": {},
    "nimi": None,
    "aika": "00:00:00",
    "vuoro": None,
    "jaljella": None,
    "havio": False,
    "voitto": False,
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


def lataa_tilastot():
    """
    Lataa pelin tilastot.
    """
    pass


def tulosta_tilastot():
    """
    Tulostaa tilastot terminaaliin.
    """
    pass


def tallenna_tilastot():
    """
    Tallentaa päättyneen pelin tiedot tilastoihin:
    """
    pass


def aloita_peli():
    """
    Aloittaa uuden pelin.
    """
    while True:
        nimi = input("Anna käyttäjänimi(max 8 merkkiä): ").strip()
        if len(nimi) > 8:
            print("Nimi on liian pitkä")
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
    luo_kentta()
    haravasto.lataa_kuvat("spritet")
    haravasto.luo_ikkuna(
        leveys=1000, korkeus=1000)
    haravasto.aseta_piirto_kasittelija(piirra_kentta)
    haravasto.aseta_hiiri_kasittelija(kasittele_hiiri)
    haravasto.aseta_toistuva_kasittelija(paivita_peli)
    haravasto.aloita()
    tila["vuoro"] = None
    tila["kentta"] = []


def luo_kentta():
    """
    Funktio joka luo valitun vaikeusasteen pohjalta miinakentän.
    """
    koko = tila["vaikeus"]["ruutuja"]
    for rivi in range(koko):
        tila["kentta"].append([])
        for sarake in range(koko):
            tila["kentta"][-1].append(" ")
    tila["naytto"] = copy.deepcopy(tila["kentta"])


def miinoita(kentta):
    """
    Asettaa kentälle N kpl miinoja satunaisiin paikkoihin.
    """
    n_miinoja = tila["vaikeus"]["miinoja"]
    tila["jaljella"] = n_miinoja
    vapaat_rudut = []
    for x in range(len(kentta)):
        for y in range(len(kentta)):
            vapaat_rudut.append((x, y))
    while n_miinoja > 0:
        x, y = random.choice(vapaat_rudut)
        vapaat_rudut.remove((x, y))
        kentta[y][x] = "x"
        n_miinoja -= 1
    for y, rivi in enumerate(kentta):
        for x, merkki in enumerate(rivi):
            if merkki == " ":
                kentta[y][x] = str(laske_minat(kentta, x, y))


def laske_minat(ruudukko, x_koordinaatti, y_koordinaatti):
    """
    Laskee annetulle kentän ruudulle montako miinaa sen ympärillä on. 
    """
    rajat = {
        "leveys_min": 0,
        "leveys_max": len(ruudukko[0]) - 1,
        "korkeus_min": 0,
        "korkeus_max": len(ruudukko) - 1
    }
    kasiteltavat = []
    rivit = [y_koordinaatti - 1, y_koordinaatti, y_koordinaatti + 1]
    sarakkeet = [x_koordinaatti - 1, x_koordinaatti, x_koordinaatti + 1]
    for rivi in rivit:
        for sarake in sarakkeet:
            if ((rajat["korkeus_min"] <= rivi <= rajat["korkeus_max"]) and
                    (rajat["leveys_min"] <= sarake <= rajat["leveys_max"])):
                kasiteltavat.append((sarake, rivi))
    miinoja = 0
    for x, y in kasiteltavat:
        merkki = ruudukko[y][x]
        if merkki == "x":
            miinoja += 1
    return miinoja


def paivita_peli(kulunut_aika):
    """
    Päivitää pelin tilannetta. Tarkastelee voito ja häviö ehtoja ja toteuttaa
    Tarvittavat toimet niiden täyttyessä. Päivittää kelloa.
    """
    pass


def kasittele_hiiri(hiiri_x, hiiri_y, hiiri_nappain, muokkaus_nappaimet):
    """
    Tätä funktiota kutsutaan, kun käyttäjä klikkaa sovellusikkunaan hiirellä.
    Tulostaa hiiren sijainnin sekä painetun napin terminaaliin.
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
        while tila["vuoro"] == None:
            miinoita(tila["kentta"])
            tila["vuoro"] = 0
        if hiiri_nappain == hiiren_nappaimet["vasen"]:
            if tila["kentta"][y][x] == "x" and tila["naytto"][y][x] != "f":
                tila["havio"] = True
            elif tila["kentta"][y][x] in MERKIT and tila["naytto"][y][x] != "f":
                tila["naytto"][y][x] = tila["kentta"][y][x]
                tila["vuoro"] += 1 
            elif tila["naytto"][y][x] == " " and tila["naytto"][y][x] != "f":
                tulvataytto(x, y)
                tila["vuoro"] += 1
        elif hiiri_nappain == hiiren_nappaimet["oikea"]:
                if tila["naytto"][y][x] == " ":
                    tila["naytto"][y][x] = "f"
                    tila["jaljella"] -= 1
                elif tila["naytto"][y][x] == "f":
                    tila["naytto"][y][x] = " "
                    tila["jaljella"] += 1


def tulvataytto(x_alku, y_alku):
    """
    Merkitsee kentällä olevat tuntemattomat ruudut turvallisiksi
    siten, että täyttö aloitetaan annetusta x, y -pisteestä.
    """
    tuntemattomat = [
        (x_alku, y_alku),
    ]
    while tuntemattomat:
        x_kasit, y_kasit = tuntemattomat.pop()
        tila["naytto"][y_kasit][x_kasit] = tila["kentta"][y_kasit][x_kasit]
        rajat = {
            "leveys_min": 0,
            "leveys_max": len(tila["naytto"][0]) - 1,
            "korkeus_min": 0,
            "korkeus_max": len(tila["naytto"]) - 1
        }
        kasiteltavat = []
        rivit = [y_kasit - 1, y_kasit, y_kasit + 1]
        sarakkeet = [x_kasit - 1, x_kasit, x_kasit + 1]
        for rivi in rivit:
            for sarake in sarakkeet:
                if ((rajat["korkeus_min"] <= rivi <= rajat["korkeus_max"]) and
                    (rajat["leveys_min"] <= sarake <= rajat["leveys_max"])):
                    # Ehtojen täyttyessä
                    kasiteltavat.append((sarake, rivi))
        for x, y in kasiteltavat:
            if tila["naytto"][y][x] == " " and tila["kentta"][y][x] in MERKIT:
                tila["naytto"][y][x] = tila["kentta"][y][x]
                continue
            elif tila["naytto"][y][x] == " " and tila["kentta"][y][x] != "x":
                tuntemattomat.append((x, y))


def piirra_kentta():
    """
    Käsittelijäfunktio, joka piirtää kaksiulotteisena listana kuvatun
    miinakentän ruudut näkyviin peli-ikkunaan. Funktiota kutsutaan aina
    kun pelimoottori pyytää ruudun näkymän päivitystä.
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
    for y, rivi in enumerate(tila["naytto"]):
        for x, merkki in enumerate(rivi):
                haravasto.lisaa_piirrettava_ruutu(
                    merkki,
                    x * 40 + tila["vaikeus"]["piirtomarginaali"],
                    y * 40 + tila["vaikeus"]["piirtomarginaali"]
                )
    haravasto.piirra_ruudut()


if __name__ == "__main__":
    nayta_paavalikko()
