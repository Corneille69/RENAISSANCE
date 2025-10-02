#include<stdio.h>
typedef struct personne personne;
struct personne

{
	char nom [20];
	char prenom [20];
	int Age;
	float Taille;
	char genre;
	
};
int main()
{
    personne P ;
	printf("Entrez votre nom:");
	scanf("%s",P.nom);
	printf("Entrez votre prenom:");
	scanf("%s",P.prenom);
	printf("Entrez votre Age:");
	scanf("%d",&P.Age);
	printf("Entrez votre Taille:");
	scanf("%f",&P.Taille);
	printf("Entrez votre genre:"); 
	getchar();
	scanf("%c",&P.genre);
	printf("\nAffichage de P\n");
	printf("%s\t%s\t%d\t%.2f\t%c",P.nom,P.prenom,P.Age,P.Taille,P.genre);
	return 0 ;
	
}