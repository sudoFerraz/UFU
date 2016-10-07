#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>

main()
{
   int canal1[2];
   int canal2[2];
   pid_t pid;

   char y=0;   
   int x=300;
   int z;

   if ( pipe(canal1) == -1 ){ printf("Erro pipe()"); return -1; }
   if ( pipe(canal2) == -1 ){ printf("Erro pipe()"); return -1; }

   pid=fork();
   
   if ( pid == 0 )
   {
	read(canal1[0],&y,sizeof(char));
	printf("Valor recebido pelo Filho do Pai=%c\n",y); fflush(stdout);
	y=y*2;
	write(canal2[1],&y,sizeof(float));
	close(canal2[1]);
   }
   else
   if (pid > 0 )
   {
	write(canal1[1],&x,sizeof(int));
	read(canal2[0],&x,sizeof(float));
	printf("Valor recebido pelo Pai do Filho=%f\n",x); fflush(stdout);
	wait(&z);
   }
 exit(0);
}
