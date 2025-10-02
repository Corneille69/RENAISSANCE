#include <stdio.h>
#include <stdlib.h>
int main()
{
	int choix;
	int facture=0;
	char reponse;
	do
	{
	
	    printf("vous etes la bienvenue dans notre entreprise!\n");
	    printf("***********Menu Hotel*********\n");
	    printf("1_pour le Riz(500FCFA)\n");
	    printf("2_pour le Haricot(300)\n");
	    printf("3_pour le spaguetti(600)\n");
	    printf("4_pour le chill(600)\n");
	    printf("5_pour le bissap(200)\n");
	    printf("6_pour l'eau(500)\n");
	    printf("Faite votre choix chers client\n");
	    scanf("%d",&choix);
	    switch(choix)
	    {
	
	   
		case 1:
			printf("vous avez choisi du riz\n");
			facture+=500;
			break;
		case 2:
			printf("vous avez choisi du Haricot\n");
			facture+=300;
			break;
		case 3:
			printf("vous avez choisi du spaguetti\n");
			facture+=600;
			break;
		case 4:
			printf("vous avez choisi du chill\n");
			facture+=600;
			break;
		case 5 :
			printf("vous avez choisi du bissap\n");
			facture+=200;
			break;
		case 6:
			printf("vous avez choisi de l'eau\n");
			facture+=500;
			break;
		default:
			printf("ce choix n'est pas pris en compte\n");
			break;
				
		}		
		printf("souhaiterez-vous continuer ?\n");
		"taper 'o'||'O'pour continuer \n"
		"autre caractere por arreter \n";
	    getchar();
		scanf("%c",&reponse);
		system("cls");
				
	}
	while (reponse=='o'||reponse=='0');
	printf("\nvous avez consommer %d FCFA",facture);
	return 0;
}