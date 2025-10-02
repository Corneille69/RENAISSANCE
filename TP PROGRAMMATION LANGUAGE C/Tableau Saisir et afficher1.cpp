#include<stdio.h>
void saisirTableau(int T[],int n);
void afficherTableau(int T[],int n);
void trieTableau(int T[],int n);
int minTableau(int)
int main()
{
	int TAB1[4],TAB2[6], TAB3[3];
	printf("saisie des elements du TAB1\n");
	saisirTableau(TAB1,4);
	printf("saisie des elements du TAB2\n");
	saisirTableau( TAB2,6);
	printf("saisie des elements du TAB3\n");
	saisirTableau(TAB3,3);
	printf("affichage des elements du TAB1\n");
	afficherTableau(TAB1,4);
	printf("affichage des elements du TAB2\n");
    afficherTableau(TAB2,6);
	printf("affichage des elements du TAB3\n");
	afficherTableau(TAB3,3);
	return 0;
}
void saisirTableau(int T[],int n)
{

	int i;
	for(i=0;i<n;i++)
	{
		printf("Entrez la valeur N %d :",i);
		
		scanf("%d",&T[i]);
	}
	
}
		void afficherTableau(int T[],int n)
{
		int i;
		printf("\n");
	    for(i=0;i<n;i++)
	{
	
		printf("%d\t:",T[i]);
		
    }	
	    printf("\n");
	    
	    void trieTableau(int T[],int n)

{
			int i;
		printf("\n");
	    for(i=0;i<n;i++)
	{
		
	}
}
{
	
