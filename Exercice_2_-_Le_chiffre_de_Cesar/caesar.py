#! /usr/bin/env python3
"""
# Exercice 2.1 - Découvrons le chiffre de César

Nous allons aujourd'hui nous lancer écrire des message secret !

## Vocabulaire

Commençons par un peu de vocabulaire:

- **Cryptologie** : La cryptologie, étymologiquement la science du secret, ne peut être vraiment considérée comme une science que depuis peu de temps. Cette science englobe la cryptographie – l’écriture secrète –, la cryptanalyse – l’analyse et l’attaque de cette dernière –, et la stéganographie – l’art de la dissimulation.
- **Cryptographie** : La cryptographie est une des disciplines de la cryptologie s’attachant à protéger des messages (assurant confidentialité, authenticité et intégrité) en s’aidant souvent de secrets ou clés.
- **Chiffrement** : Le chiffrement est un procédé de cryptographie grâce auquel on souhaite rendre la compréhension d’un document impossible à toute personne qui n’a pas la clé de (dé)chiffrement. Ce principe est généralement lié au principe d’accès conditionnel.
- **Chiffrer** : L’action de procéder à un chiffrement.
- **Déchiffrer** : En informatique et en télécommunications, déchiffrer consiste à retrouver le texte original (aussi appelé clair) d’un message chiffré dont on possède la clé de (dé)chiffrement.
- **Décrypter** : Décrypter consiste à retrouver le texte original à partir d’un message chiffré sans posséder la clé de (dé)chiffrement. Décrypter ne peut accepter d’antonyme : il est en effet impossible de créer un message chiffré sans posséder de clé de chiffrement.

Attention il y a quelques mots qu'on entend souvent mais qui sont faux :

- **Crypter / Cryptage** : Le terme « cryptage » et ses dérivés viennent du grec ancien κρυπτός, kruptos, « caché, secret ». Cependant, le Référentiel Général de Sécurité de l’ANSSI qualifie d’incorrect « cryptage ». En effet, la terminologie de cryptage reviendrait à chiffrer un fichier sans en connaître la clé et donc sans pouvoir le déchiffrer ensuite. Le terme n’est par ailleurs pas reconnu par le dictionnaire de l’Académie française.
- **Encrypter / Déencrypter** : Le terme « encrypter » et ses dérivés sont des anglicismes. Donc, nan, on ne les utilise pas non plus.
- **Chiffrage** : Celui-là, c’est le pompon, la cerise sur le gâteau. Le chiffrage, c’est évaluer le coût de quelque chose. ABSOLUMENT RIEN à voir avec le chiffrement. Et pourtant, parfois, on le voit.
- **Coder / Encoder / Décoder** : Coder / Encoder signifie “Constituer (un message, un énoncé) selon les règles d’un système d’expression − langue naturelle ou artificielle, sous une forme accessible à un destinataire.” En informatique il s’agit d’une façon d’écrire les mêmes données, mais de manière différente (ex. en base64, en hexadécimal, avec des codes correcteurs d’erreurs etc…). Ce procédé est facilement inversible (il n’y a aucune notion de clé dans ces opérations), il n’y a aucune vocation à assurer la confidentialité, ce n’est donc pas du chiffrement.

## Explications

Nous allons commencer par faire ce qu'il y a de plus simple : nous allons **chiffrer** puis **déchiffrer** un message. Pour cela nous allons utiliser une méthode extrêmement ancienne le "chiffre de César". Jules César l'utilisait pour ses correspondances... donc aux allentour du premier siècle avant JC.

Comme on code en anglais on va parler de :

- texte clair --> plain text
- texte chiffré --> cipher text
- alphabet clair --> plain alphabet
- alphabet chiffré --> cipher alphabet (souvent juste appelé "cipher")
- clé (de chiffrement) --> key

Le chiffre de César consiste simplement à décaler les lettres de l'alphabet de quelques crans vers la droite ou la gauche.

## Exemple

Par exemple, décalons les lettres de 3 rangs vers la droite (on dit qu'il a une clé de +3) :

key: +3
plain:  ABCDEFGHIJKLMNOPQRSTUVWXYZ
cipher: XYZABCDEFGHIJKLMNOPQRSTUVW

Ce qui va donner par exemple (on convertit tout en majuscule et on garde les espaces inchangés car c'est plus simple comme ça):

plain text:  Ave Caesar morituri te salutant
cipher text: XSB ZXBPXO JLOFQROF QB PXIRQXKQ

## Tes outils

Pour réaliser ça tu auras besoin de 2 fonctions qui permettent de traiter les lettre comme leurs valeur ASCII (encodage standard des caractères sous forme de nombre). Si tu te demandes pourquoi 'A' correspond au numéro 65 au lieu de 1... c'est juste qu'on a mis toutes les lettres minusculesla ponctuation et autres bizarreries avant les lettres :

>>> ord('A')
65
>>> ord('B')
66
>>> ord('C')
67

Et on peut faire l'opération inverse :

>>> chr(65)
'A'
>>> chr(66)
'B'
>>> chr(67)
'C'

## Petit piège à éviter

Je t'invite tout de même à faire attention... dans le chiffre de César l'alphabet "boucle" donc il va falloir que tu trouve un moyen pour éviter que Z se transforme en n'importe quoi par exemple :

>>> ord('Z')
90
>>> chr(90)
'Z'
>>> chr(90+3)
']'
"""
import string
import logging
import sys
from typing import Dict



def crack_key(cypher_text: str) -> int:
    """Finde key"""
    ALPHABET = list(string.ascii_uppercase)
    CYPHER_TEXT = list(cypher_text)
    list_occurence_by_letter = []
    for letter in ALPHABET:
        occurrence = CYPHER_TEXT.count(letter)
        list_occurence_by_letter.append(occurrence)
    INDEX_LETTER_MOST_OCCURENCE = list_occurence_by_letter.index(
        max(list_occurence_by_letter)
    )
    LIKELY_TO_BE_E = ALPHABET[INDEX_LETTER_MOST_OCCURENCE]
    LIKELY_KEY = ord(LIKELY_TO_BE_E) - ord("E")
    return LIKELY_KEY


def do_decipher(cypher_text: str, key: int) -> str:
    """Decipher text """
    ALPHABET = list(string.ascii_uppercase)

    CYPHER_TEXT = list(cypher_text)
    cypher_alphabet = list(string.ascii_uppercase)
    if key > 0:
        cypher_alphabet.extend(cypher_alphabet[:key])
        del cypher_alphabet[:key]
    elif key < 0:
        letter_to_deplace = cypher_alphabet[key:]
        letter_to_deplace.extend(cypher_alphabet)
        cypher_alphabet = letter_to_deplace
        del cypher_alphabet[key:]

    decypher_text = []

    for counter, letter_to_crack in enumerate(CYPHER_TEXT):
        if letter_to_crack not in ALPHABET:
            decypher_text.append(letter_to_crack)
        else:
            decypher_text.append(ALPHABET[cypher_alphabet.index(letter_to_crack)])
    decypher_text = "".join(decypher_text)
    return decypher_text


def exercise_2_2():
    INTERCEPTED_TEXT = (
        "KPIVKM L'MABIQVO : "
        "RMCVM LMUWVMBBM, MTTM I CVM IXXIZMVKM PCUIQVM, UIQA LWBMM "
        "LM LMCF XMBQBMA KWZVMA ACZ TM NZWVB MB LM LMCF IQTMA LMUWVQIYCMA, "
        "BGXM KPICDM-AWCZQA, LIVA TM LWA. UITOZM AMA IQTMA, MTTM VM AIQB YCM "
        "XTIVMZ. LCZIVB TMCZA WXMZIBQWVA, MTTM I XWCZ VWU LM KWLM JTIKSJQZL."
    )

    EXPECTED_TEXT = (
        "Chance d'Estaing : "
        "Jeune demonette, elle a une apparence humaine, mais dotee "
        "de deux petites cornes sur le front et de deux ailes demoniaques, "
        "type chauve-souris, dans le dos. Malgre ses ailes, elle ne sait que "
        "planer. Durant leurs operations, elle a pour nom de code Blackbird."
    )

    print("************* Exercise  2.2 *************\n\n")
    print("****** Let's break Caesar's cypher ******\n\n")
    print("Intercepted text    :", INTERCEPTED_TEXT)
    print("Expacted clear text :", EXPECTED_TEXT)
    print("Key                 :", "???")
    print()

    print("Let's break it")
    CRACKED_KEY = crack_key(INTERCEPTED_TEXT)
    print("Cracked key      :", CRACKED_KEY)
    print()

    print("Let's use the cracked key (will it work?!)")
    CRACKED_TEXT = do_decipher(INTERCEPTED_TEXT, CRACKED_KEY)
    print("Cracked text:", CRACKED_TEXT)
    print()

    SUCCESS = EXPECTED_TEXT.upper() == CRACKED_TEXT
    print("Did it worked?", "OK :)" if SUCCESS else "Nope :(")


def main():

    exercise_2_2()


if __name__ == "__main__":
    main()
