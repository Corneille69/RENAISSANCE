#include <stdio.h>
int main()
{
	int T[10]={10,34,-21,5,-12,-23,0,-30,4,31,};
	int i;
	printf("les valeurs positifs \n");
	for(i=0;i<10;i++)
	{
		if(T[i]>=0)
		{
			printf("%d\t",T[i]);
		}
	}
	
	printf("\nles valeurs negatives \n");
	for(i=0;i<10;i++)
	{
		if(T[i]<0)
		{
			printf("%d\t",T[i]);
		}
	}
	return 0;
}