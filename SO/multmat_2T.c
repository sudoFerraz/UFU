#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>


#define LINES 5000
#define COLS 5000
#define NR_THREADS 2


int M1[LINES][COLS];
int M2[LINES][COLS];
int M3[LINES][COLS];


void * thread_par(void *);
void * thread_impar(void *);

main()
{
  pthread_t tids[NR_THREADS];
  register int i,j;

   /* Inicializa M1, M2, M3 */
   for(i=0;i<LINES;i++)
    for(j=0;j<COLS;j++)
     {
	M1[i][j]=1;
	M2[i][j]=2;
	M3[i][i]=0;	
     }
  
   /* Cria as 2 Threads */
   pthread_create(&tids[0],NULL,thread_par,NULL);
   pthread_create(&tids[1],NULL,thread_impar,NULL);

   /* Aguarda o termino das 2 Threads */
   pthread_join(tids[0],NULL);
   pthread_join(tids[1],NULL);

    
   /* Imprime o conteudo de M3 
   for(i=0;i<LINES;i++)
   {
    for(j=0;j<COLS;j++)
     {
	printf("M3[%d][%d]=%d\n",i,j,M3[i][j]);	
     }
   }
     printf("pressione qualquer tecla para continuar \n");
     getchar(); */
   exit(1);
}
   

void * thread_par(void *ptr)
{
  register int l,c, C,L=0, soma=0, w=0, r=0;

  for(l=0;l<LINES;l+=2)
  {
   for(C=0;C<COLS;C++)
    { 
      for(c=0; c<LINES; c++)
       {   
      	  soma = soma + M1[l][c] * M2[L][C];
          L++;
       }
      M3[l][C]=soma;
      L=0;
      soma=0;
      w++;
    }
  }
}

void * thread_impar(void *ptr)
{
  register int l,c, C,L=0, soma=0, w=0, r=0;

  for(l=1;l<LINES;l+=2)
  {
   for(C=0;C<COLS;C++)
    { 
      for(c=0; c<LINES; c++)
       {   
      	  soma = soma + M1[l][c] * M2[L][C];
          L++;
       }
      M3[l][C]=soma;
      L=0;
      soma=0;
      w++;
    }
  }
}


