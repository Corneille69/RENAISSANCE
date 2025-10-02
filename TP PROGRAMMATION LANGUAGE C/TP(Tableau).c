#include <stdio.h>
int main()
{
	float Notes[5]={4,5,8,6,2};
	int i;
	for (i=0;i<5;i++)
	{
		printf("Entrez la Notes N%d\t",i);
		scanf("%f",&Notes[i]);
		
	}
	
	
	for (i=0;i<5;i++)
	{
		printf("%.2f\t",Notes[i]);
	}
	
	return 0;
}