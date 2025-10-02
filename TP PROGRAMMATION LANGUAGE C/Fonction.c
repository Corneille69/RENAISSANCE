#include <stdio.h>
int add(int a,int b);
int soust(int a,int b);
int multiplication(int a,int b);
int main()

{
	int x=6,y=9,z;
	z=add(x,y);
	printf("La somme de %d et %d est %d\n",x,y,z);
	z=soust(x,y);
	printf("La soustraction de %d et %d est %d\n",x,y,z);
	z=multiplication(x,y);
	printf("La soustraction de %d et %d est %d\n",x,y,z);
	return 0;
}
int add(int a,int b)
{
    int c;
    c=a+b;
	return c;
}
int soust(int a,int b)
{
	int c;
	c=a-b;
	return c;
}
int multiplication(int a,int b)
{
	int c;
	c=a*b;
	return c;

}
