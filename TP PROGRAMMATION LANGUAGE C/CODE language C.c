#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct Livre {
    int id;
    char titre[100];
    char auteur[100];
    int annee;
    int disponible; 
    struct Livre* suivant;
} Livre;

Livre* tete = NULL;

// 🔁 Créer un nouveau livre
Livre* creerLivre(int id, char* titre, char* auteur, int annee, int disponible) {
    Livre* nouveau = (Livre*)malloc(sizeof(Livre));
    nouveau->id = id;
    strcpy(nouveau->titre, titre);
    strcpy(nouveau->auteur, auteur);
    nouveau->annee = annee;
    nouveau->disponible = disponible;
    nouveau->suivant = NULL;
    return nouveau;
}

// ➕ Insertion en tête
void insererEnTete(Livre* nouveau) {
    nouveau->suivant = tete;
    tete = nouveau;
}

// ➕ Insertion en queue
void insererEnQueue(Livre* nouveau) {
    if (tete == NULL) {
        tete = nouveau;
    } else {
        Livre* temp = tete;
        while (temp->suivant != NULL)
            temp = temp->suivant;
        temp->suivant = nouveau;
    }
}

// 📜 Afficher tous les livres
void afficherLivres() {
    Livre* temp = tete;
    if (temp == NULL) {
        printf("La bibliothèque est vide.\n");
        return;
    }
    while (temp != NULL) {
        printf("ID: %d | Titre: %s | Auteur: %s | Année: %d | %s\n",
            temp->id, temp->titre, temp->auteur, temp->annee,
            temp->disponible ? "Disponible" : "Emprunté");
        temp = temp->suivant;
    }
}

// 🔍 Rechercher un livre par ID
Livre* rechercherParID(int id) {
    Livre* temp = tete;
    while (temp != NULL) {
        if (temp->id == id)
            return temp;
        temp = temp->suivant;
    }
    return NULL;
}

// 🔍 Rechercher un livre par titre
Livre* rechercherParTitre(char* titre) {
    Livre* temp = tete;
    while (temp != NULL) {
        if (strcmp(temp->titre, titre) == 0)
            return temp;
        temp = temp->suivant;
    }
    return NULL;
}

// ❌ Supprimer un livre par ID
void supprimerParID(int id) {
    Livre *temp = tete, *precedent = NULL;
    while (temp != NULL && temp->id != id) {
        precedent = temp;
        temp = temp->suivant;
    }
    if (temp == NULL) {
        printf("Livre avec ID %d introuvable.\n", id);
        return;
    }
    if (precedent == NULL) {
        tete = temp->suivant;
    } else {
        precedent->suivant = temp->suivant;
    }
    free(temp);
    printf("Livre supprimé avec succès.\n");
}

// ✏️ Modifier un livre
void modifierLivre(int id) {
    Livre* livre = rechercherParID(id);
    if (livre == NULL) {
        printf("Livre introuvable.\n");
        return;
    }
    printf("Nouveau titre : ");
    scanf(" %[^\n]", livre->titre);
    printf("Nouvel auteur : ");
    scanf(" %[^\n]", livre->auteur);
    printf("Nouvelle année : ");
    scanf("%d", &livre->annee);
    printf("Modification terminée.\n");
}

// 📚 Emprunter un livre
void emprunterLivre(int id) {
    Livre* livre = rechercherParID(id);
    if (livre == NULL) {
        printf("Livre introuvable.\n");
        return;
    }
    if (!livre->disponible) {
        printf("Le livre est déjà emprunté.\n");
    } else {
        livre->disponible = 0;
        printf("Livre emprunté avec succès.\n");
    }
}

// 🔁 Retourner un livre
void retournerLivre(int id) {
    Livre* livre = rechercherParID(id);
    if (livre == NULL) {
        printf("Livre introuvable.\n");
        return;
    }
    if (livre->disponible) {
        printf("Le livre est deja disponible.\n");
    } else {
        livre->disponible = 1;
        printf("Livre retourne avec succes.\n");
    }
}

// 📋 Menu principal
void menu() {
    int choix, id, annee, pos;
    char titre[100], auteur[100];
    while (1) {
        printf("\n**** BIENVENUE DANS LA BIBLIOTHEQUE DE L'UNIVERSITE BIT DE KDG'****\n");
        printf("\n Veuillez remplir les donnees suivants :\n");
        
        printf("1. Ajouter un livre\n");
        printf("2. Afficher les livres\n");
        printf("3. Rechercher par ID\n");
        printf("4. Rechercher par titre\n");
        printf("5. Supprimer un livre\n");
        printf("6. Modifier un livre\n");
        printf("7. Emprunter un livre\n");
        printf("8. Retourner un livre\n");
        printf("9. Quitter\n");
        printf("Votre choix : ");
        scanf("%d", &choix);
        switch (choix) {
            case 1:
                printf("ID : "); scanf("%d", &id);
                printf("Titre : "); scanf(" %[^\n]", titre);
                printf("Auteur : "); scanf(" %[^\n]", auteur);
                printf("Annee : "); scanf("%d", &annee);
                printf("1 pour tete , 2 pour queue : "); scanf("%d", &pos);
                if (pos == 1)
                    insererEnTete(creerLivre(id, titre, auteur, annee, 1));
                else
                    insererEnQueue(creerLivre(id, titre, auteur, annee, 1));
                break;
            case 2:
                afficherLivres(); break;
            case 3:
                printf("ID : "); scanf("%d", &id);
                Livre* l1 = rechercherParID(id);
                if (l1)
                    printf("Livre trouve : %s par %s (%d) [%s]\n", l1->titre, l1->auteur, l1->annee, l1->disponible ? "Disponible" : "Emprunte");
                else
                    printf("Aucun livre trouve.\n");
                break;
            case 4:
                printf("Titre : "); scanf(" %[^\n]", titre);
                Livre* l2 = rechercherParTitre(titre);
                if (l2)
                    printf("Livre trouve : %s par %s (%d) [%s]\n", l2->titre, l2->auteur, l2->annee, l2->disponible ? "Disponible" : "Emprunte");
                else
                    printf("Aucun livre trouve.\n");
                break;
            case 5:
                printf("ID : "); scanf("%d", &id);
                supprimerParID(id); break;
            case 6:
                printf("ID du livre a modifier : "); scanf("%d", &id);
                modifierLivre(id); break;
            case 7:
                printf("ID : "); scanf("%d", &id);
                emprunterLivre(id); break;
            case 8:
                printf("ID : "); scanf("%d", &id);
                retournerLivre(id); break;
            case 9:
                exit(0);
            default:
                printf("Choix invalide.\n");
        }
    }
}

int main() {
    menu();
    return 0;
}