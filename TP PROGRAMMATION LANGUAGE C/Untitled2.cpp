#include <stdlib.h>
typedef struct Notes Notes ;
struct Notes

{
	float N;
	Notes *suivant;
	
};
void AjouterDebutListe(Notes **L,float x);
void AfficherListe(Notes *L);
int main()

{
	Notes *L=NULL;
	float x; 
	char reponse;
	do
	
	{
		printf("Entrer une valeur:");
		scanf("%f",&x);
		AjouterDebutListe(&L,x);
		printf("Souhaiteriez-vous continuer? \n0 ou o pour continuer");
		getchar();
		scanf("%c",&reponse);
		
	}
	while(reponse==o)
}
