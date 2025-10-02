#include <stdio.h>

// Définition de la structure Animal
typedef struct {
    char nom[50];
    char espece[50];
    int age;
} Animal;

int main() {
    // Création d'une liste (tableau) de 3 animaux
    Animal liste_animaux[3] = {
        {"Rex","Chien", 5},
        
        {"Mimi", "Chat", 6},
        
        {"Tweety", "Oiseau", 9}
    };

    // Affichage des animaux
    for (int i = 0; i < 3; i++) {
        printf("Animal %d\t : Nom=%s\n, Espece=%s\n, Age=%d\n",
               i + 1,
               liste_animaux[i].nom,
               liste_animaux[i].espece,
               liste_animaux[i].age);
    }

    return 0;
}