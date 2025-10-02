#include <stdio.h>

int main()
{
	int x=5;
	int *p;
	p=&x;
	
	printf("x=%d\n",x);
	*p=*p+5;
	printf("x=%d\n",x);
	
	return 0;
	
}