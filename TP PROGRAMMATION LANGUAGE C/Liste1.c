
#include <stdlib.h>
typedef struct Notes Notes ;
struct Notes

{
	float N;
	Notes *suivant;
	
};
int main()
{
	Notes *L=NULL;
	Notes *E1=(Notes*)malloc(sizeof(Notes));
	Notes *L=NULL;
	Notes *E2=(Notes*)malloc(sizeof(Notes));
	Notes *L=NULL;
	Notes *E3=(Notes*)malloc(sizeof(Notes));
		Notes *L=NULL;
	Notes *E4=(Notes*)malloc(sizeof(Notes));
	
	E1->N=7;
	L=E1;
	E1->suivant=NULL
	
	E2->N=17;
	E1->suivant=E2;
	E2->suivant=NULL;
	
	E3->N=78;
	E2->suivant=E3;
	E3->suivant=NULL;
	
	E4->N=72;
	E3->suivant=E4;
	E4->suivant=L;
	L=E4;
	
	Notes *i=L;
	while(i!=NULL)
	{
		printf("%.2f=>",i->N);
		i=i->suivant;
	}
	return 0;
}