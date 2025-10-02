
 
#include <stdio.h>
#include <stdlib.h>
#include"fonction.h"
typedef struct Eleve Eleve;

int main(){

	Eleve E[3];
	int i,j;
	for(i=0,i<3,i++)
	{
	printf("Entrer LE nom:");
	scanf("%s",E.nom);
	printf("Entrer votre prenom:");
	scanf("%s",E.prenom);
	for(i=0,i<5,i++)
	}
	
	{
		printf("Entrer la note [%d]",i+1);
	    scanf("%f",&E.Matiere[i]);
	    
	    	
	}
	printf("Le nom est %s\n",E.nom);
	printf("Le prenom est %s\n",E.prenom);
	printf("Math\tAnglais\tSVT\EPS\tPC\n");
	for(i=0,i<5,i++)
	
	{
		printf("%.2f\t",E.Matiere[i]);
	}
	return 0;

}