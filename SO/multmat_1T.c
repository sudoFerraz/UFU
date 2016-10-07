#include <stdio.h>
#include <stdlib.h>

#define LINES 5000
#define COLS 5000


int M1[LINES][COLS];
int M2[LINES][COLS];
int M3[LINES][COLS];


main()
{

  register int i,j;
  register int l,c, C,L=0, soma=0, w=0, r=0;

   /* Inicializa M1, M2, M3 */
   for(i=0;i<LINES;i++)
    for(j=0;j<COLS;j++)
     {
	M1[i][j]=1;
	M2[i][j]=2;
	M3[i][i]=0;	
     }
  

  for(l=0;l<LINES;l++)
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

   
   /* Imprime o conteudo de M3 */
   for(i=0;i<LINES;i++)
   {
    for(j=0;j<COLS;j++)
     {
	printf("M3[%d][%d]=%d\n",i,j,M3[i][j]);	
     }
   }
     printf("pressione qualquer tecla para continuar \n");
     getchar(); 
   exit(1);
}
   

