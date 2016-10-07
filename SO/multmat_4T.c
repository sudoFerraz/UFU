#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>


#define LINES 5000
#define COLS 5000
#define NR_THREADS 4


int M1[LINES][COLS];
int M2[LINES][COLS];
int M3[LINES][COLS];


void * thread_1(void *);
void * thread_2(void *);
void * thread_3(void *);
void * thread_4(void *);

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
   pthread_create(&tids[0],NULL,thread_1,NULL);
   pthread_create(&tids[1],NULL,thread_2,NULL);
   pthread_create(&tids[2],NULL,thread_3,NULL);
   pthread_create(&tids[3],NULL,thread_4,NULL);

   /* Aguarda o termino das 4 Threads */
   pthread_join(tids[0],NULL);
   pthread_join(tids[1],NULL);
   pthread_join(tids[2],NULL);
   pthread_join(tids[3],NULL);

    
/* Imprime o conteudo de M3 
   for(i=0;i<LINES;i++)
   {
    for(j=0;j<COLS;j++)
     {
	printf("M3[%d][%d]=%d\n",i,j,M3[i][j]);	
     }
   }
     printf("pressione qualquer tecla para continuar \n");
     getchar();*/
   exit(1);
}
   

void * thread_1(void *ptr)
{
  register int l,c, C,L=0, soma=0, w=0, r=0;

  for(l=0;l<1250;l++)
  {
   for(C=0;C<5000;C++)
    { 
      for(c=0; c<5000; c++)
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

void * thread_2(void *ptr)
{
  register int l,c, C,L=0, soma=0, w=0, r=0;

  for(l=1250;l<2500;l++)
  {
   for(C=0;C<5000;C++)
    { 
      for(c=0; c<5000; c++)
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

void * thread_3(void *ptr)
{
  register int l,c, C,L=0, soma=0, w=0, r=0;

  for(l=2500;l<3750;l++)
  {
   for(C=0;C<5000;C++)
    { 
      for(c=0; c<5000; c++)
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

void * thread_4(void *ptr)
{
  register int l,c, C,L=0, soma=0, w=0, r=0;

  for(l=3750;l<5000;l++)
  {
   for(C=0;C<5000;C++)
    { 
      for(c=0; c<5000; c++)
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

