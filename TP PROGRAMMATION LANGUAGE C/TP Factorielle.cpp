#include <stdio.h>
int main()
{
	int N,P,A;
	printf("Entrez un entier:");
	scanf("%d",&N);
	printf("%d!=");
	for(P=1;P<=N;P++)
	{
		A=A*P;
		printf("%d",P);
		if(P==N)
		{
			continue;
		}
		printf("*");
		
	}
	printf("=%d",A);
	
	return 0;
}