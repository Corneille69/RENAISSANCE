#include <stdio.h>

int main()
{
	float *Notes;
	int p,i,N;
	printf("Entrer la taille du tableau : \n");
	scanf("%d",&p);
	Notes=(float*)calloc(p, sizeof(float));
	for(i=0;i<p;i++)
	{
		printf("Entrer la Notes N%d :",i);
		scanf("%f",(Notes+i));
	}
	for(i=0;i<p;i++)
	{
		printf("%.2f\t",*(Notes+i));
		
	}
	printf("Entrer la nombre de la case a ajjouter au tableau\n");
	scanf("%d",&N);
	Notes=(float*)realloc(Notes,N*sizeof(float));
	for(i=p;i<p+N;i++)
	{
		printf("Entrer la Notes N%d :",i+1);
		scanf("%f",(Notes+i));
	}
	for(i=0;i<p+N;i++)
	{
		printf("%.2f\t",*(Notes+i));
		
	}

	return 0;
}