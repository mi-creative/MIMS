# _________________________________________________________________________#
# JV - 19/02/13															  #
# _________________________________________________________________________#
# Script 																  #
# _________________________________________________________________________#

# __________________________ Paramètres Initiaux __________________________#

# ___ Selection sur l'établi du modèle à analyser (en l'état: MAS, SOL, REF)
# _____ le résultat sera visualisable dans la fenêtre
# _____ d'exécution du script en sous l'onglet 'Outputs'

# _________________________________________________________________________#

import physicsGenerator.topologyGenerator as topoGen



### Conversion depuis un couple (raideur modale et viscosité modale) vers une fréquence propre
def oscillator_stiffnessvisco_2_frequencies (stiffness_list, viscos_list, simfreq) :
    freq_list = []
    a = 2*3.14159265358979323846
    i = 0
    for x in stiffness_list :
        if x < 0 or x >4 :
            print("Diverge")
        else :
            freq_list.append(simfreq/a*np.arccos((2-(x+viscos_list[i])) / (2*np.sqrt(1-viscos_list[i]))))
    i += 1
    return freq_list


def oscillator_damping_2_taux_amortissement (viscos_list, simfreq) :
    taux_list = []
    for x in viscos_list :
        taux_list.append(-2/(simfreq*np.log(1-x)))
    return taux_list




########################################################################################################################
### Visualisation des matrices topologiques M et K (Z supposée proportionnelle)
### Pour utilisation : Selectionner l'ensemble de module que vous souhaitez analyser (pour l'heure constitué uniquement de MAS SOL et REF)
### Executez le script, le résulatat sera visualisable dans la fenetre d'execution du script en tant qu'Outputs.
### Version avec affichage numérique des paramètres du modèle
################################################ Initialisation  #######################################################





################ CREATION DES LISTES DE SELECTIONS ################



########################################################################################################################
### Nous devons différencier les Mas connectées à d'autres Mas, des Mas connectées à des Sol.
### Le bout de script suivant permet, étant donnée une liste de SOL et une liste de REF :
### - l'obtention d'une liste (list_Mas_connectee_Sol) des masses connectées à un module SOL
### - l'obtention d'une liste (list_Ref_connectant_Mas_a_Sol) du REF liant les masses de la liste précédente à même valeur d'indexe à un SOL
### - l'obtention d'une liste (list_Ref_MasMas) des REF ne connectant que des MAS entre elles. Liste qui servira pour la suite du script.
########################################################################################################################



########################################################################################################################
### Creation d'une liste de couples MAS-REF (liste_MasRefMas) connectes à la MAS correspondante a meme valeur d'index (listMas)
### Utilisation de la liste list_Ref_MasMas épurée des connections MAS-REF pour ne conciderer que les connections entre MAS
########################################################################################################################



########################################################################################################################
### Creation d'une liste de couples MAS-REF (liste_MasRefMas) connectes à la MAS correspondante a meme valeur d'index (listMas)
########################################################################################################################

# afficher "listMas"
# afficher $listMas
# afficher " "

# afficher "liste_MasRefMas"
# afficher $liste_MasRefMas
# afficher " "

# afficher "list_Mas_connectee_Sol"
# afficher $list_Mas_connectee_Sol
# afficher " "

# afficher "list_Ref_connectant_Mas_a_Sol"
# afficher $list_Ref_connectant_Mas_a_Sol
# afficher " "

########################################################################################################################
### Creation des matrices topologiques
########################################################################################################################
### Création de M, K, Z
########################################################################################################################


import numpy as np

M = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]])

K = np.array([[0.02, -0.01, 0], [-0.01, 0.02, -0.01], [0, -0.01, 0.02]])

Z = np.array([[0.0002, -0.0001, 0], [-0.0001, 0.0002, -0.0001], [0, -0.0001, 0.0002]])

#print(M, K, Z)


# ######################################################################################################################
# ### Anlyse Modale
# ######################################################################################################################

m = np.diag(M)
D = np.diag(np.sqrt(m))
invD = np.diag(1/np.sqrt(m))

Matrice_Kprim = invD.dot(K).dot(invD)
Matrice_Zprim = invD.dot(Z).dot(invD)

raideaurs_modales, Matrice_de_Passage = np.linalg.eig(Matrice_Kprim)
print(raideaurs_modales)
print(Matrice_de_Passage)

viscosite_modales = np.diag(np.transpose(Matrice_de_Passage).dot(Matrice_Zprim).dot(Matrice_de_Passage))
print(viscosite_modales)

print(oscillator_stiffnessvisco_2_frequencies(raideaurs_modales, viscosite_modales, 44100))
print(oscillator_damping_2_taux_amortissement(viscosite_modales, 44100))

#topoGen.createTriangleMembrane(5, "triangle", 1.0, 0.01, 0.0001, 0, 0.00001)
topoGen.createHexagonaleMembrane(3, "haxagone", 1.0, 0.01, 0.0001, 0, 0.0000)

