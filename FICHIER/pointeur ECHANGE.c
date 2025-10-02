#include <stdio.h>
void Echange(int *A,int *B);
int main()

{
	int A,B;
	printf("entrer la premiere valeur:\n");
	scanf("%d",&A);
	printf("entrer la deuxieme valeur:\n");
	scanf("%d",&B);
	printf("Avant\n");
	printf("A=%d\n",A);
	printf("B=%d\n",B);
	Echange(&A,&B);
	printf("Apres\n");
	printf("A=%d\n",A);
	printf("B=%d\n",B);
	return 0;
	
}
void Echange (int *A, int *B)
{
	int c;
	c=*A;
	*A=*B;
	*B=c;
}