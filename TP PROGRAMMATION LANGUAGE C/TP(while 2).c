#include <stdio.h>
int main()
{
	int i,n,r;
	printf("Entrez un entier:");
	scanf("%d",&n);
	i=0;

	while(i<=10)
	{
		r=i*n;
		printf("%d*%d=%d\n",n,i,r);
		i++;
		
	}
	return 0;
}