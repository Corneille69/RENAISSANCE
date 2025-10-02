#include <stdio.h>
int main()
{
	
	float Notes[5];
	float summ= 0;
	float Moyennes;
	int i; 
	printf("Afficher la moyennes des eleves\n:");
	for(i=0;i<5;i++)
	{
		
		printf("Entrez la Notes des eleves %d\n:",i+1);
		scanf("%f",&Notes[i]);
	}
	for(i=0;i<5;i++)
	{
		summ+=Notes[i];
		
	}
	Moyennes=summ/5;
	printf("La moyenne de la clsse est:%.2f",Moyennes);
	return 0;
}