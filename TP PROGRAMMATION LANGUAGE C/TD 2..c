#include <stdio.h>

#define L4
int main()
{
	int T[6];
	int i;
	int S=0;
	for(i=0;i<6;i++)
	{
		for(i=0;i<6;i++)
		{
			printf("Entrez la valeurs est N%d :",i);
			scanf("%d",&T[i]);
		}
		for(i=0;i<6;i++)
		{
			S+=T[i];
			
		}
		printf("La somme est %d :",S);
		int max;
		int min,
		pmax=0,
		pmin=0;
		min=max=T[0];
		for(i=0;i<6;i++)
		{
			if(T[i]<min)
			{
				T[i]=min;
				pmin=i;
				
			}
		}
		printf("la valeur minimum est :%d\n",min,pmin);
		printf("la valeur : %d en la position %d est le minimum\n ");
		
		
		for(i=0;i<6;i++)
		{
			if(T[i]<max)
			{
				T[i]<max;
				max=T[i];
			
				pmax=i;
			}
		}
		printf("la valeur maximum est :%d\n",max,pmax);
		    printf("la valeur :%d en la position %d est le maximum\n");
			int K,L,N;
			printf(" les valeurs apres le trie\n");
			
			for(i=0;i<6;i++)
			{
				
				
				printf("%d\t",T[i]);
				
		
			}	
			
			
	}
	
	
	

    return 0;

}	
		
		
	    
		
		
		
		
		
	
	

	
	
	
