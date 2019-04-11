"""
Pythonilla toteutettu versio miinaharava pelistä.
"""
import random

import haravasto

TILA = {
    "kentta": [],
    "vaikeus": None,
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
    except KeyboardInterrupt:
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
    pass


def luo_kentta():
    """
    Funktio joka luo annettujen parametrien pohjalta miinakentän.
    """
    pass


def miinoita(kentta, vapaat_rudut, n_miinoja):
    """
    Asettaa kentälle N kpl miinoja satunaisiin paikkoihin.
    """
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
    elif hiiri_nappain == hiiren_nappaimet["keski"]:
        print("Hiiren nappia keski painettiin kohdassa {x}, {y}".format(
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
    haravasto.aloita_ruutujen_piirto()
    for y, rivi in enumerate(TILA["kentta"]):
        for x, merkki in enumerate(rivi):
            if merkki == "x":
                haravasto.lisaa_piirrettava_ruutu("x", x * 40, y * 40)
            else:
                haravasto.lisaa_piirrettava_ruutu(" ", x * 40, y * 40)
    haravasto.piirra_ruudut()


if __name__ == "__main__":
    nayta_paavalikko()
