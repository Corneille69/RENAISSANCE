#include <stdio.h>
#include <stdlib.h>
int main()
{
	double a,b,c,x;
	printf("Application-polynome du second degree\n");
	printf("Entrez a:");
	scanf("%l",&a);
	printf("Entrez b:");
	scanf("%l",&b);
	printf("Entrez c:");
	scanf("%l",&c);
	printf("Entrez la valeur de x pour evaluer le polynome:");
	scanf("%lf",&x);
	evaluer_polynome(a,b,c,x)
	calculer_polynome(a,b,c,x);
	return 0;
}