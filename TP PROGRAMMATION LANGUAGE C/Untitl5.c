#include <stdio.h>
#include <math.h>
int main()
{
	float a,b,c,Delta;
	float x1,x2,x3;
	printf("Entrez la valeur de a :");
	scanf("%f",&a);
	printf("Entrez la valeur de b :");
	scanf("%f",&b);
	printf("Entrez la valeur de c:");
	scanf("%f",&c);
	Delta =pow(b,2)-4*a*c;
	printf("Delta=%f\n",Delta);
	if (Delta>=0)
	{
		x1=(-b-sqrt(Delta))/ (2*a);
		x2=(-b+sqrt(Delta))/(2*a);
		printf("x1=%.2f\tx2=%.2f",x1,x2);
	}
	else
	{
		printf("pas de solution dans R");
	}
}