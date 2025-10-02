#include<stdio.h>
#include<string.h>
int main()
{
	char nom[19]="OUEDRAOGO";
	char prenom[17]="RAYIM-WEND";
	int L,K;
	printf("nom est :%s \n",nom);
	printf("prenom est :%s \n",prenom);
	strcat(nom,prenom);
	L= strlen(nom);
	K= strlen(prenom);
	
	printf("\nnom est :%s et \nle nombre de caractere est %d\n",nom,L);
	printf("\prenom est :%s et \nle nombre de caractere est %d\n",prenom,K);
	return 0;
}