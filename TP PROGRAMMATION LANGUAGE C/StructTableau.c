#include <stdio.h>
 typedef struct Etudiant Etudiant ;
 struct Etudiant
 {
 	char Nom[20];
 	char Prenom[20]; 
 	char ville[20];
 	int Matricule;
 	int passeword;
 	
 };
 int main()
 {
 	Etudiant *ET;
 	int N,i;
 	printf("Entrer le nombre d'etudiant :");
 	scanf("%d",&N);
 	ET=(Etudiant*)malloc(N*sizeof(Etudiant));
 	for(i=0;i<N;i++)
 	
 	{
 		printf("Entrer le nom de l'etudiant %d",i+1);
 		scanf("%s",ET[i].Nom);
 		
 		printf("Entrer le prenom de l'etudiant %d",i+1);
 		scanf("%s",ET[i].Prenom);
 		
 		printf("Entrer la ville de l'etudiant %d",i+1);
 		scanf("%s",ET[i].ville);
 		
 		printf("Entrer le Matricule de l'etudiant %d",i+1);
 		scanf("%s",&ET[i].Matricule);
 		
 		printf("Entrer le passeword de l'etudiant %d",i+1);
 		scanf("%s",&ET[i].passeword);
	}
	for(i=0;i<N;i++)
	{
	 	printf("%s\t",ET[i].Nom);
	 	printf("%s\t",ET[i].Prenom);
	 	printf("%s\t",ET[i].ville);
	 	printf("%d\t",ET[i].Matricule);
	 	printf("%d\n",ET[i].passeword);
	 	
	}
	free(ET);
 	return 0;
 }