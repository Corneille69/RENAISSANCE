#include <stdio.h>
float produitscalaire(float T[],float R[],int n);
int main()
{
	float U[4]={1,1,0,6,},V[4]={2,0,1,4};
	float PS;
	PS=produitscalaire(U,V,4);
	printf("Le produit scalaire est %.2f",PS);
	return 0;
}
float produitscalaire(float T[],float R[],int n)
{
	int i;
	float P=0;
	for (i=0;i<n;i++)
	{
		P=P+T[i]*R[i];
		
	}
	return P;
	
}