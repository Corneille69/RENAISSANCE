#include <stdio.h>
#include <string.h>
struct eleve{ 
char nom[10],prenom[10];
float note[5]
};
{

int main()
   {
		struct eleve E[3];
		int i ,j;
		printf("Entrer Le nom de l'etudiant %d:",i+1);
		scanf("%s",E[i].nom);
		printf("Entrer le prenom de l'etudaint %d:",i+1);
		scanf("%s",E[i].prenom);
		for(j=0;j<5;j++)
	    {
			printf("Entrer la note[%d] de l'eleve n[%d]:",j+1,i+1);
			scanf("%f",&E[i].Matiere[j]);
		
	    }
   }
	printf("Nom\tprenom\tManth\tAnglais\tSVT\tPC\n");
	for(i=0,i<3,i++);
   {
		printf("%s\t",E[i].nom)
		printf("%s\t",E[i].prenom)
		for(j=0;j<5;j++)
	    {
		printf("%d.2f\t",E[i].Matiere[j]);
	    }
   }
return0
}