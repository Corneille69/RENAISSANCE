#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct Contact {
    char nom[50];
    char prenom[50];
    char telephone[20];
    char email[100];
    char adresse[100];
    struct Contact* suivant;
} Contact;

Contact* tete = NULL;

// Fonction pour créer un contact
Contact* creerContact() {
    Contact* nouveau = (Contact*)malloc(sizeof(Contact));
    printf("Nom : ");
    scanf(" %[^\n]", nouveau->nom);
    printf("Prenom : ");
    scanf(" %[^\n]", nouveau->prenom);
    printf("Telephone : ");
    scanf(" %[^\n]", nouveau->telephone);
    printf("Email : ");
    scanf(" %[^\n]", nouveau->email);
    printf("Adresse : ");
    scanf(" %[^\n]", nouveau->adresse);
    nouveau->suivant = NULL;
    return nouveau;
}

// Ajouter contact en fin ou en ordre alphabétique (par nom)
void ajouterContact() {
    Contact* nouveau = creerContact();

    // Insertion en tête si liste vide ou avant le premier (ordre par nom)
    if (tete == NULL || strcmp(nouveau->nom, tete->nom) < 0) {
        nouveau->suivant = tete;
        tete = nouveau;
        return;
    }

    Contact* courant = tete;
    while (courant->suivant != NULL && strcmp(nouveau->nom, courant->suivant->nom) > 0) {
        courant = courant->suivant;
    }
    nouveau->suivant = courant->suivant;
    courant->suivant = nouveau;
}

// Affichage de tous les contacts
void afficherContacts() {
    if (tete == NULL) {
        printf("Carnet vide.\n");
        return;
    }

    Contact* courant = tete;
    while (courant != NULL) {
        printf("\nNom: %s\nPrénom: %s\nTéléphone: %s\nEmail: %s\nAdresse: %s\n",
               courant->nom, courant->prenom, courant->telephone,
               courant->email, courant->adresse);
        courant = courant->suivant;
    }
}

// Rechercher un contact par nom ou téléphone
void rechercherContact() {
    char critere[100];
    int trouve = 0;
    printf("Entrer le nom ou le numéro à rechercher : ");
    scanf(" %[^\n]", critere);

    Contact* courant = tete;
    while (courant != NULL) {
        if (strcmp(courant->nom, critere) == 0 || strcmp(courant->telephone, critere) == 0) {
            printf("\n[Contact trouve]\nNom: %s\nPrenom: %s\nTelephone: %s\nEmail: %s\nAdresse: %s\n",
                   courant->nom, courant->prenom, courant->telephone,
                   courant->email, courant->adresse);
            trouve = 1;
        }
        courant = courant->suivant;
    }

    if (!trouve) {
        printf("Aucun contact trouve.\n");
    }
}

// Supprimer un contact par nom
void supprimerContact() {
    char nom[50];
    printf("Entrer le nom du contact a supprimer : ");
    scanf(" %[^\n]", nom);

    Contact* courant = tete;
    Contact* precedent = NULL;

    while (courant != NULL && strcmp(courant->nom, nom) != 0) {
        precedent = courant;
        courant = courant->suivant;
    }

    if (courant == NULL) {
        printf("Contact introuvable.\n");
        return;
    }

    if (precedent == NULL) {
        tete = courant->suivant;
    } else {
        precedent->suivant = courant->suivant;
    }

    free(courant);
    printf("Contact supprime avec succes.\n");
}

// Modifier un contact par nom
void modifierContact() {
    char nom[50];
    printf("Entrer le nom du contact a modifier : ");
    scanf(" %[^\n]", nom);

    Contact* courant = tete;

    while (courant != NULL && strcmp(courant->nom, nom) != 0) {
        courant = courant->suivant;
    }

    if (courant == NULL) {
        printf("Contact introuvable.\n");
        return;
    }

    printf("Modification du contact %s :\n", nom);
    printf("Nouveau prenom : ");
    scanf(" %[^\n]", courant->prenom);
    printf("Nouveau telephone : ");
    scanf(" %[^\n]", courant->telephone);
    printf("Nouvel email : ");
    scanf(" %[^\n]", courant->email);
    printf("Nouvelle adresse : ");
    scanf(" %[^\n]", courant->adresse);
    printf("Contact modifie avec succes.\n");
}

// Menu principal
void menu() {
    int choix;
    do {
        printf("\n *** BIENVENU dans le Carnet d'adresses ***\n");
        printf("1. Ajouter un contact\n");
        printf("2. Afficher tous les contacts\n");
        printf("3. Rechercher un contact\n");
        printf("4. Supprimer un contact\n");
        printf("5. Modifier un contact\n");
        printf("0. Quitter\n");
        printf("Votre choix : ");
        scanf("%d", &choix);

        switch (choix) {
            case 1: ajouterContact(); break;
            case 2: afficherContacts(); break;
            case 3: rechercherContact(); break;
            case 4: supprimerContact(); break;
            case 5: modifierContact(); break;
            case 0: printf("Fermeture du programme.\n"); break;
            default: printf("Choix invalide.\n");
        }
    } while (choix != 0);
}

int main() {
    menu();
    return 0;
}
