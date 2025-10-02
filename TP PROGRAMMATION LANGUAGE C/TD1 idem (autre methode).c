#include <stdio.h>
void PosTab(int T[],int n);
void NegTab(int T[],int n);
int main()
{
	int T[10]={10,34,-21,5,-12,-23,9,-30,4,31,};
	printf("les valeurs positives \n");
	PosTab(T,10);
	printf("\nles valeurs negatives \n");
	NegTab(T,10);
	return 0;
}
void PosTab(int T[],int n)
{

    int i;
    for(i=0;i<10;i++)
	{
		if(T[i]>=0)
		{
			printf("%d\t",T[i]);
		}
	}

}

void NegTab(int T[],int n)
{
	int i;
    for(i=0;i<10;i++)
	{
		if(T[i]<0)
		{
			printf("%d\t",T[i]);
		}
	}
}


