#include <stdio.h>
#include <stdlib.h>


int main()
{
	int **M;
	int L,C,i,j;
	printf("Entrer le nombre de la ligne : \n");
	scanf("%d",&L);
	printf("Entrer une valeur le nombre de la colonne : \n");
	scanf("%d",&C);
	M=(int**)malloc(L*sizeof(int*));
	for(i=0;i<L;i++)
	{
		M[i]=(int*)malloc(C*sizeof(int));
	}
	for(i=0;i<L;i++)
	
	{
		for(j=0;j<C;j++)
		{
			printf("%d\t",M[i][j]);
			
		}
		printf("\n");
		
	}
	return 0;
	
}