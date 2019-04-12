"""
Pythonilla toteutettu versio miinaharava pelistä.
"""
import random
import datetime
import copy

import haravasto

VAIKEUSASTEET = {
    "helppo": {"ruutuja": 25, "miinoja": 10, "piirtomarginaali": 150},
    "normaali": {"ruutuja": 49, "miinoja": 20, "piirtomarginaali": 112},
    "vaikea": {"ruutuja": 100, "miinoja": 30, "piirtomarginaali": 50}
}

tila = {
    "kentta": [],
    "naytto": [],
    "vaikeus": {},
    "nimi": None,
    "aika": "00:00:00",
    "vuoro": "0",
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
        leveys=500, korkeus=600)
    haravasto.aseta_piirto_kasittelija(piirra_kentta)
    haravasto.aseta_hiiri_kasittelija(kasittele_hiiri)
    haravasto.aloita()
    tila["kentta"] = []


def luo_kentta():
    """
    Funktio joka luo valitun vaikeusasteen pohjalta miinakentän.
    """
    koko = int(tila["vaikeus"]["ruutuja"] ** (1 / 2))
    for rivi in range(koko):
        tila["kentta"].append([])
        for sarake in range(koko):
            tila["kentta"][-1].append(" ")
    tila["naytto"] = copy.deepcopy(tila["kentta"])
    miinoita(tila["kentta"])


def miinoita(kentta):
    """
    Asettaa kentälle N kpl miinoja satunaisiin paikkoihin.
    """
    n_miinoja = tila["vaikeus"]["miinoja"]
    vapaat_rudut = []
    for x in range(len(kentta)):
        for y in range(len(kentta)):
            vapaat_rudut.append((x, y))
    while n_miinoja > 0:
        x, y = random.choice(vapaat_rudut)
        vapaat_rudut.remove((x, y))
        kentta[y][x] = "x"
        n_miinoja -= 1


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
    if hiiri_nappain == hiiren_nappaimet["vasen"]:
        print("Hiiren nappia vasen painettiin kohdassa {x}, {y}".format(
            x=hiiri_x,
            y=hiiri_y
        ))
    elif hiiri_nappain == hiiren_nappaimet["oikea"]:
        print("Hiiren nappia oikea painettiin kohdassa {x}, {y}".format(
            x=hiiri_x,
            y=hiiri_y
        ))


def piirra_kentta():
    """
    Käsittelijäfunktio, joka piirtää kaksiulotteisena listana kuvatun
    miinakentän ruudut näkyviin peli-ikkunaan. Funktiota kutsutaan aina
    kun pelimoottori pyytää ruudun näkymän päivitystä.
    """
    haravasto.tyhjaa_ikkuna()
    haravasto.piirra_tausta()
    haravasto.piirra_tekstia("Aika:", 50, 500)
    haravasto.piirra_tekstia(tila["aika"], 50, 450)
    haravasto.piirra_tekstia("Vuoro:", 300, 500)
    haravasto.piirra_tekstia(tila["vuoro"], 300, 450)
    haravasto.aloita_ruutujen_piirto()
    for y, rivi in enumerate(tila["naytto"]):
        for x, merkki in enumerate(rivi):
                haravasto.lisaa_piirrettava_ruutu(
                    merkki,
                    x * 40 + tila["vaikeus"]["piirtomarginaali"],
                    y * 40 + tila["vaikeus"]["piirtomarginaali"]
                )
    haravasto.piirra_ruudut()


def tulvataytto(ruudukko, x_alku, y_alku):
    """
    Merkitsee kentällä olevat tuntemattomat ruudut turvallisiksi
    siten, että täyttö aloitetaan annetusta x, y -pisteestä.
    """
    if ruudukko[y_alku][x_alku] == "x":
        return
    tuntemattomat = [
        (x_alku, y_alku),
    ]
    while tuntemattomat:
        x_kasittely, y_kasittely = tuntemattomat.pop()
        ruudukko[y_kasittely][x_kasittely] = "0"
        rajat = {
            "leveys_min": 0,
            "leveys_max": len(ruudukko[0]) - 1,
            "korkeus_min": 0,
            "korkeus_max": len(ruudukko) - 1
        }
        kasiteltavat = []
        rivit = [y_kasittely - 1, y_kasittely, y_kasittely + 1]
        sarakkeet = [x_kasittely - 1, x_kasittely, x_kasittely + 1]
        for rivi in rivit:
            for sarake in sarakkeet:
                if ((rajat["korkeus_min"] <= rivi <= rajat["korkeus_max"]) and
                    (rajat["leveys_min"] <= sarake <= rajat["leveys_max"])):
                    # Ehtojen täyttyessä
                    kasiteltavat.append((sarake, rivi))

        for x, y in kasiteltavat:
            merkki = ruudukko[y][x]
            if merkki == " ":
                tuntemattomat.append((x, y))


if __name__ == "__main__":
    nayta_paavalikko()
