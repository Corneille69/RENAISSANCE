#include<stdio.h>
#include<string.h>
int main()
{
	char nom[15]="ZERBO";
	char prenom[15]="OCORN";
	if(strcmp(nom,prenom)>0)
	{
		printf("%s est superieur a %s",nom,prenom);
		
	}
	
		else if (strcmp(nom,prenom)<0)
		{
			printf("%s est superieur a %s",nom,prenom);
		}
		else
		{
			printf("%s est identique a %s",nom,prenom);
		}
	
	return 0;

}