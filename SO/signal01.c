#include <signal.h>
#include <stdio.h>

void rotina(int p)
{
	printf("Nao vou terminar\n");
}

main()
{
	int i=0;
	signal(SIGINT, rotina);

	while(1){ printf("%d\n",i++); }
} 
