#include<stdio.h>
typedef struct personne personne ; 
struct personne
{
	char nom[20];
	char prenom[20];
	int age;
	float taille;
	char genre;
	
};
int main ()
{
	personne p[4];
	int i;
	printf("Entrez la valeur des personne\n");
	for(i=0;i<4;i++)
	{
		printf("Entrez le nom de la personne p[%d]\n",i);
		scanf("%s",p[i].nom);
		printf("Entrez le prenom de la personne p[%d]\n",i);
		scanf("%s",p[i].prenom);
		printf("Entrez l'age de la personne p[%d]\n",i);
		scanf("%d",&p[i].age);
		printf("Entrez la taille de la personne p[%d]\n",i);
		scanf("%f",&p[i].taille);
		printf("Entrez le genre de la personne p[%d]\n",i);
		getchar;
		scanf("%c",&p[i].genre);
		{
			printf("%s\t%s\t%dans\%2.fmetres\t%c\t");
		}

    }

}

