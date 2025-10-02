#include <stdio.h>
#define L 2
#define C 3
int main()
{

	int  T[L][C];
	int  K[L][C];
	int  M[L][C];
	int i,j;
	printf("Saisi de la code Matrice T\n");
	for(i=0;i<L;i++)
	{
		for (j=0;j<C;j++)
	    {
	    	printf("Entrez la valeur code T[%d][%d]:",i,j);
	    	scanf("%d",&T[i][j]);
	   
	    }
	for(i=0;i<L;i++)
	{
		for (j=0;j<C;j++)	
		{
			M[i][j]=T[i][j]+K[i][j];
			
		}
	printf("Affichage de la code MatriceT\n");
	for(i=0 ;i<L;i++)
	{
		for (j=0;j<C;j++)
		{
			printf("%d\t",T[i][j]);
		}
		printf("\n");
		
	printf("Affichage de la code MatriceK\n");
	for(i=0 ;i<L;i++)
	{
		for (j=0;j<C;j++)
		{
			printf("%d\t",K[i][j]);
		}
		printf("\n");
		
    printf("Affichage de la code MatriceM\n");
	for(i=0 ;i<L;i++)
	{
		for (j=0;j<C;j++)
		{
			printf("%d\t",M[i][j]);
	
		}
		printf("\n");			
	}
	
	return 0;
	
	}
}	
