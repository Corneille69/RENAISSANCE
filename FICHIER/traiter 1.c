#include<stdio.h>
typedef struct personne personne;
struct personne
{
	char nom[20];
	char prenom[20];
	int Age;
	float taille;
	char genre ;
};
int main()
{
	personne p[4];
	int i;
	printf("la saisie des informations des personnes illustrer\n",i);
	for(i=0;i<4;i++)
	{
		printf("entrez le nom de la personne p[%d]\n",i);
		scanf("%s",p[i].nom);
		printf("entrez le prenom de la personne p[%d]\n",i);
		scanf("%s",p[i].prenom);
		printf("entrez l'age de la personne p[%d]\n",i);
		scanf("%d",&p[i].Age);
		printf("entrez la taile de la personnep[%d]\n",i);
		scanf("%2.f",&p[i].taille);
		printf("entrer le genre de la personne p[%d]\n",i);
		getchar;
		scanf("%c",p[i].genre);
		{
			printf("%s\t%s\t%dans\t%2.fm\t%chumain\n",p[i].nom,p[i].prenom,p[i].Age,p[i].taille,p[i].genre);
		}
		
		
	}
}

