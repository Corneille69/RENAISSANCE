HG#include <stdio.h>
int main()
{
	int x=5;
	FILE *F=NULL;
	F=fopen("Data.txt","w");
	if(F!=NULL)
	{
		fprintf(F,"Bonjour tu a %d ans ",x);
	}
	fclose(F);
	return 0;
}
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        																																																																																									