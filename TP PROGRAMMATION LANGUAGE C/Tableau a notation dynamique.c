#include <stdio.h>

int main()
{
	float *Notes;
	int p,i;
	printf("Entrer la taille du tableau : \n");
	scanf("%d",&p);
	Notes=(float*)calloc(p*sizeof(float));
	for(i=0;i<p;i++)
	{
		printf("Entrer la Notes N%d :",i);
		scanf("%f",(Notes+i));
	}
	for(i=0;i<p;i++)
	{
		printf("%.2f\t",*(Notes+i));
		
	}
	free(Notes);
	return 0;
}