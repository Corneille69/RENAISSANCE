#include <stdio.h>
#define L 2
#define C 3
int main()

{
   int T[L][C];
   int i,j;
   for (i=0;i<L;i++)

   {
	   for(j=0;j<C;i++)
	
       {
    	   printf("Entrez la valeur T[%d][%d]:",i,j);
    	   scanf("%d",&T[i][j]);
	   }
   }
   for (i=0;i<L;i++)
   {
   	   for(j=0;j<C;i++)
	   {
	   	   printf("%d\t",T[i][j]);
	   }
	   printf("\n")	;
	
	}
	return 0;   
}