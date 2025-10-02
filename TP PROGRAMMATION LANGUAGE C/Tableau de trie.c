#include <stdio.h>
#define L 2
#define C 3
int main()
{
	int T[5];
	int i,j,k;
	printf("\nSaisi des elements du tableau \n");
	for (i=0;i<5;i++)
	{
		printf("Entrez la valeur %d:",i);
		scanf("%d",&T[i]);
	}
	printf("\nLe tableau avant le trie\n");
	for (i=0;i<5;i++)
	{
		printf("%d\t",T[i]);
		
	}
	for (i=0;i<5;i++)
	{
		for(j=0;j<5;j++)
		{
			if(T[i]<T[j])
			{
				k=T[i];
				T[i]=T[j];
				T[j]=k;
			}
		}
	}
	printf("\nLe tableau apres le trie\n");
	for (i=0;i<5;i++)
	{
		printf("%d\t",T[i]);
		
	}
	return 0;
}