#include<stdio.h>
struct personne

{
	char nom [20];
	char prenom [20];
	int Age;
	float Taille;
	char genre;
};
int main()
{
    struct personne P[4] ;
    
    int i,j;
    printf("saisie des informations des personnes\n");
    for(i=0;i<4;i++)
    {
    	printf("Entrez le nom de la personne: P[%d]",i);
    	scanf("%s",P[i].nom);
    	printf("Entrez prenom de la personne P[%d]\n",i);
    	scanf("%s",P[i].prenom);
    	printf("Entrez Age de la personne P[%d]\n",i);
    	scanf("%d",&P[i].Age);
    	printf("Entrez Taille de la personne P[%d]\n",i);
    	scanf("%f",&P[i].Taille);
	    printf("Entrez genre de la personne P[%d]\n",i); 
	    getchar();
	    scanf("%c",&P[i].genre);
    	
	}
	
	
	printf("\nAffichage des personnes de plus de 50ans\n");
	for(i=0;i<4;i++)
	{
		if(P[i].Age>=50)
	
	   {
		    printf("%s\t%s\t%dans\t%.2fm\t%c\n",P[i].nom,P[i].prenom,P[i].Age,P[i].Taille,P[i].genre);
	   }
	
	}   
	printf("\nAffichage des informations sur le genre masculin \n");
	for(i=0;i<4;i++)
	{
		if(P[i].genre=='M')
	
	   {
		   printf("%s\t%s\t%dans\t%.2fm\t%c\n",P[i].nom,P[i].prenom,P[i].Age,P[i].Taille,P[i].genre);
	
	
	   }
	}   
	
	printf("\nAffichage des informations sur le genre feminin \n");
	for(i=0;i<4;i++)
	{
		if(P[i].genre=='F')
	
	   {
		   printf("%s\t%s\t%dans\t%.2fm\t%c\n",P[i].nom,P[i].prenom,P[i].Age,P[i].Taille,P[i].genre);
	
	
	   }
   for(i=0;i<4;i++)
   {
	   	   for(j=i;j<4;j++)
	   	   {
			 
	   	   	    if(strcmp(P[i].nom,P[j].nom,P[j].nom)>0)
	   	   	    {
	   	   	  	    TP=P[i];
	   	   	  	    P[i]=P[j];
	   	   	  	    P[j]=TP;
	   	   	  	}
	   	   	}  	
	}
	   	   	  
	}	
		
printf("\nAffichage des personnes dans l'ordre alphabetiques \n");
for(i=0;i<4;i++)
	
	
{
		printf("%s\t%s\t%dans\t%.2fm\t%c\n",P[i].nom,P[i].prenom,P[i].Age,P[i].Taille,P[i].genre);
		
}
	return 0 ;
	
}
	
	

	
	
