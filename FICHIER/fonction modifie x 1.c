

#include <stdio.h>
int modifiex();

int main()
int x=5;


{
	printf("%d\n",x);
	modifiex();
	printf("%d",x);
	return 0;
}

	int modifiex()
{
	return x++;
}