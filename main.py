#
# s'il n'y a pas de lien urgent à couper (porte présente sur un chemin de profondeur 1), 
# alors couper les liens des noeuds connectés directement à plusieurs portes (les + proches du virus) car ils ne seront pas gérables si le virus atteint ce noeud
# pb conséquent : gérer les portes présentes sur les chemins de profondeur 2, définir une priorisaton entre le lien urgentProfondeur2 
# et le noeud chargé en fonction de la distance de celui-ci



import sys
from collections import Counter

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

# n: the total number of nodes in the level, including the gateways
# l: the number of links
# e: the number of exit gateways
n, l, e = [int(i) for i in input().split()]
liens  = []
portes = []

for i in range(l):
    # n1: N1 and N2 defines a link between these nodes
    n1, n2 = [int(j) for j in input().split()]
    liens.append([n1,n2])

for i in range(e):
    ei = int(input())  # the index of a gateway node
    portes.append(ei)

noeuds = []
for i in range(n):
    noeuds.append(i)
for lien in liens:
    for noeud in noeuds:
        if noeud in portes:
            noeuds.remove(noeud)

def liensDuNoeud(noeud):
    res = []
    for lien in liens:
        if noeud in lien:
            res.append(lien)
    return res

def cheminsDuNoeud(noeud):
    res = []
    for lien in liensDuNoeud(noeud):
        chemin = lien if lien[0] == noeud else [noeud, lien[0]]
        res.append(chemin)
    return res

def reductionChemin(chemin):
    res = chemin
    for i in range(len(res[:-1])-1):
        if res[i] == res[i+1]:
            res.remove(res[i])
    return res

def lienDuChemin(chemin):
    for lien in liens:
        if lien == chemin or lien == chemin[::-1]:
            return lien
        
def porteDuLien(lien):
    for noeud in lien:
        if noeud in portes:
            return noeud

def cheminsPossibles(noeud, prof):
    res = [[noeud]]
    for i in range(prof):
        chemins = res
        res = []
        for chemin in chemins:
            for c in cheminsDuNoeud(chemin[-1]):
                res.append(reductionChemin(chemin+c))
    return res
    
def printLien(lien):
    print(str(lien[0]) + " " + str(lien[1]))


def liensSensibles(si,prof):
    res         = []
    countPortes = []
    for c in cheminsPossibles(si,prof):
        for porte in portes:
            if porte in c:
                # alerte car une porte se trouve sur un chemin !
                chemin = c[-2:]
                lien   = lienDuChemin(chemin)
                porte  = porteDuLien(lien)
                nbCheminsPorte = len(cheminsDuNoeud(porte))
                # print(
                    # "chemin sensible : " + str(c)
                #     "\tporte : " + str(porte) +
                #     "\tlien associé : " + str(lien) +
                #     "\tnbCheminsPorte : " + str(nbCheminsPorte) +
                #     " --> " + str(cheminsDuNoeud(porte))
                    # , file=sys.stderr, flush=True)

                res.append(lien)
    return res
    

def noeudDuLienDeLaPorte(lien):
    for noeud in lien:
        if (noeud in portes == False):
            return noeud


def most_common_value(lst):
    count = Counter(lst)
    return max(count, key=count.get)

def lienPrioritaire(liens):
    # pas de priorité si n_portes < 5
    if e < 5:
        return liens[0]
    else:
        #retourner parmi les liens celui contenant la porte la plus chargée (avec le + de liens)
        charges = []
        for lien in liens:
            for noeud in lien:
                if noeud in portes:
                    charges.append(len(liensDuNoeud(noeud)))
        
        # vérifier s'il a une charge plus grande que toutes les autres et renvoyer le lien correspondant
        if charges.count(max(charges)) == 1:
            return liens[charges.index(max(charges))]
        else:
            # s'il y'a des charges max égales, alors il faut prioriser autrement :
            # parmi les liens, chercher les noeuds qui possèdent le + de liens vers des portes
            noeudsTemp = []
            for lien in liens:
                for noeud in lien:
                    if noeud not in portes:
                        noeudsTemp.append(noeud)
            
            noeudPrioritaire = most_common_value(noeudsTemp)
            
            for lien in liens:
                if noeudPrioritaire in lien:
                    return lien

# game loop
while True:
    si = int(input())  # The index of the node on which the Bobnet agent is positioned this turn

    prof = 0
    while len(liensSensibles(si, prof)) == 0:
        prof += 1
        # print("prof : " + str(prof), file=sys.stderr, flush=True)


    print("sensibles : " + str(liensSensibles(si, prof)), file=sys.stderr, flush=True)

    lien_a_cuter = lienPrioritaire(liensSensibles(si, prof))
    liens.remove(lien_a_cuter)
    printLien(lien_a_cuter)
