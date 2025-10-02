#include<stdio.h>
int main()

{

	int choix;
	int facture=0;
	char reponse;
	do

    {
		printf("*******MENU DE L'HOTEL LA prosperite***********\n ");
		printf("1-pour du pizza(4500FCFA)\n");
		printf("2-pour du Gapal (1200FCFA)\n");
		printf("3-pour du Riz sauce tomate(1000FCFA)\n");
		printf("4-pour de la soupe du boeuf (600FCFA)\n");
		printf("5- pour du poulet roti(6000FCFA)\n");
		
		printf("6-pour du vin de bissape(500FCFA)\n");
		printf("7- pour du jus (300FCFA)\n");
		
		
		scanf("%d",&choix);
		switch(choix)
        {
				case 1:
					printf("1- vous avez choisi du pizza\n");
					facture+=4500;
				    break;
				case 2:
					printf("2- vous avez choisi du Gapal\n");
					facture+=1200;
					break;
				case 3:
					printf("1- vous avez choisi du Riz sauce tomate\n");
					facture+=1000;
					break;
				case 4:
					printf("1- vous avez choisi de la soupe du boeuf\n");
					facture+=600;
					break;
				case 5:
					printf("1- vous avez choisi du poulet roti\n");
					facture+=6000;
					break;
				case 6:
					printf("1- vous avez choisi du vin de bissap\n");
					facture+=500;
					break;
				case 7:
					printf("1- vous avez choisi du JUS \n");
					facture+=300;
					break;
				default:
				printf("ce choix n'a pas ete pris en compte\n")	;
				break;
		}
		printf("souhaiterez vous continuer ?\n");
		"taper 'o' || 'O' pour continuer \n"
		"Autre caracter pour arreter \n";
		getchar();
		scanf("%c" ,&reponse);
		system("cls");
	
   }
   while (reponse=='o'|| reponse=='O');
   printf("Nous avons consommer %d FCFA",facture);
   return 0;
}
