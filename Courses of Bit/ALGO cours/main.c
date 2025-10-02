#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_PRODUCTS 1000
#define HEIGHT_NAME 50

typedef struct Product Product;
struct Product{
    int id;
    char name[HEIGHT_NAME];
    int quantity;
};

Product stock[MAX_PRODUCTS];
int nbProducts = 0;


void chargerStock()
 {
    FILE *file = fopen("stock.txt", "r");
    if (file == NULL) return;

    while (fscanf(file, "%d %s %d", &stock[nbProducts].id, stock[nbProducts].name, &stock[nbProducts].quantity) == 3)
	{
        nbProducts++;
    }
    fclose(file);
}


void saveStock() {
    FILE *file = fopen("stock.txt", "w");
    for (int i = 0; i < nbProducts; i++)
	{
        fprintf(file, "%d %s %d\n", stock[i].id, stock[i].name, stock[i].quantity);
    }
    fclose(file);
}


void add()
 {
    if (nbProducts >= MAX_PRODUCTS) 
	{
        printf(" The stock is full.\n");
        return;
    }

    Product p;
    printf(" ID: ");
    scanf("%d", &p.id);
    printf("Name: ");
    scanf("%s", p.name);
    printf("Quantity : ");
    scanf("%d", &p.quantity);

    stock[nbProducts++] = p;
    printf("Product added successfully.\n");
}


void edit()
 {
    int id;
    printf("Enter the product that you want to edit ID: ");
    scanf("%d", &id);

    for (int i = 0; i < nbProducts; i++)
	 {
        if (stock[i].id == id)
		 {
            printf("New name : ");
            scanf("%s", stock[i].name);
            printf("New quantity : ");
            scanf("%d", &stock[i].quantity);
            printf("Product edited.\n");
            return;
        }
    }
    printf("Product no found.\n");
}


void suppress() 
{
    int id;
    printf("ID of the product to delete : ");
    scanf("%d", &id);

    for (int i = 0; i < nbProducts; i++)
	 {
        if (stock[i].id == id) 
		{
            for (int j = i; j < nbProducts - 1; j++) 
			{
                stock[j] = stock[j + 1];
            }
            nbProducts--;
            printf("Product deleted!");
            return;
        }
    }
    printf("Product no found.\n");
}


void display()
 {
    printf("\nList of products :\n");
    for (int i = 0; i < nbProducts; i++) 
	{
        printf("ID: %d  | Name: %s  | Quantity: %d  kg\n", stock[i].id, stock[i].name, stock[i].quantity);
    }
}


void search()
 {
    char criteria[HEIGHT_NAME];
    printf("Entrer the name or the ID of the product to find : ");
    scanf("%s", criteria);

    int id = atoi(criteria);
    for (int i = 0; i < nbProducts; i++)
	 {
        if (stock[i].id == id || strcmp(stock[i].name, criteria) == 0) 
		{
            printf("Product founded : ID=%d , Name=%s , Quantity=%d\n", stock[i].id, stock[i].name, stock[i].quantity);
            return;
        }
    }
    printf("Product no founded.\n");
}


void menu()
 {
    int choice;
    do {
        printf("\n--- MENU ---\n");
        printf("1. Add a new product\n");
        printf("2. Edit a product\n");
        printf("3. Delete a product\n");
        printf("4. Display all the products\n");
        printf("5. Research a product\n");
        printf("6. Save and quit\n");
        printf("Your choice : ");
        scanf("%d", &choice);

        switch (choice)
		 {
            case 1: add();
			break;
            case 2: edit();
			break;
            case 3: suppress(); 
			break;
            case 4: display(); 
			break;
            case 5: search(); 
			break;
            case 6: saveStock(); 
			printf("Data saved. Bye ! \n"); 
			break;
            default: printf("Invalide choice. \n");
        }

    } while (choice != 6);
}

int main()
 {
    chargerStock();
    menu();
    return 0;
}
