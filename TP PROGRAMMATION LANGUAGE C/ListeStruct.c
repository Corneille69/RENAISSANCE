#include <stdio.h>
#include <stdlib.h>
typedef struct ordinateur Ordinateur;
struct Ordinateur

{
	char NomP[20];
	char Marque[20];
	char Processeur[20];
	int Ram;
	
	
};

typedef struct Element  Element;
struct  Element

{
	Ordinateur 0;
	Element *suivant ;
	
};
void AjouterDebutListe(Element **L,Ordinateur x);
void AfficherListe(Element *L);
int main()
 {
	Element *Liste=NULL;
	Ordinateur 01,02,03,04;
	SaisirOrdinateur(&01);
	getchar();
	
	SaisirOrdinateur(&02);
	getchar();
	SaisirOrdinateur(&03);
	getchar();
	SaisirOrdinateur(&04);
	
	AjouterDebutListe(&L,01);
	AjouterDebutListe(&L,02);
	AjouterDebutListe(&L,03);
	AjouterDebutListe(&L,04);
	return 0;
 	
 }
 void AjouterDebutListe(Element **L,Ordinateur x)
 {
	Element *Ordi=(Element*)malloc(sizeof(Element));
	Ordi->O=x;
	Ordi->suivant=*L;
	*L=Ordi;
}
void AfficherListe(Element *L)
{
	if(L=NULL)
	{
		printf("\nla liste est vide"\n);
	}
	else
	{
		Element *i=L;
		printf("\n-------------------------------------------------------------------------------------------------------------|\n");
		printf("\nNomP\t|Marque\t|Processeur\t|Ram\t|\n");
		printf("\n-------------------------------------------------------------------------------------------------------------|\n");
		while(i!=NULL)
		{
			printf("%s\t|%s\t|%s\t\%d\t|",i->0.Marque,i->0.Processeur,i->0.Ram);
			printf("\n-------------------------------------------------------------------------------------------------------------|\n");
			i=i->suivant;
			
		}
	}
}

void SaisieOrdinateur(Ordinateur *x)
{
	printf("Entrer le Nom du propietaire:");
	gets(x->NomP);
	printf("Entrer la Marque:");
	gets(x->Marque);
	printf("Entrer le type de Processeur:");
	gets(x->Processeur);
	printf("Entrer la capacite de la Ram:");
	scanf("%d",&x->Ram)
	
}














