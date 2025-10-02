#include <stdio.h>
 int main()
{
	int N,i,R;
	printf("Entrez un entier:");
	scanf("%d",&N);
	for(i=0;i<=10;i++)
	{
		R=i*N;
		printf("%d*%d=%d\n",N,i,R);
		
		
	}
	return 0;
}