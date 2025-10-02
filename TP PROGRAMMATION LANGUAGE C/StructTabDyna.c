#include <stdlib.h>
 typedef struct Etudiant Etudiant ;
 struct Etudiant
 {
 	char Nom[20];
 	char Prenom[20]; 
 	char ville[20];
 	int Matricule;
 	int passeword;
};
void SaisirEtudiant(Etudiant *E,int N);
void AfficherEtudiant(Etudiant *E,int N);
int main()
{
	Etudiant *ET;
 	int N,i;
 	printf("Entrer le nombre d'etudiant :");
 	scanf("%d",&N);
 	ET=(Etudiant*)malloc(N*sizeof(Etudiant));
 	SaisirEtudiant(ET, N);
  	AfficherEtudiant(ET, N);
  	free(ET);
  	return 0;
  	
}
void SaisirEtudiant(Etudiant *E,int N) 
{
	int i;
	for(i=0;i<N;i++)
	{
		printf("Entrer le nom de l'etudiant %d:",i+1);
 		scanf("%s",E[i].Nom);
 		
 		printf("Entrer le prenom de l'etudiant %d:",i+1);
 		scanf("%s",E[i].Prenom);
 		
 		printf("Entrer la ville de l'etudiant %d:",i+1);
 		scanf("%s",E[i].ville);
 		
 		printf("Entrer le Matricule de l'etudiant %d:",i+1);
 		scanf("%s",&E[i].Matricule);
 		
 		printf("Entrer le passeword de l'etudiant %d:",i+1);
 		scanf("%s",&E[i].passeword);
 		
 	
	}
		
 		
}  
void AfficherEtudiant(Etudiant *E,int N)		
{
	
	int i;
	for(i=0;i<N;i++)
	{
		printf("%s\t",E[i].Nom);
	 	printf("%s\n",E[i].Prenom);
	 	printf("%s\n",E[i].ville);
	 	printf("%s\t",E[i].Matricule);
	 	printf("%s\t",E[i].passeword);
	 	
		
	}
	 	
	
	free(E);
 	return 0;
	
}

 	