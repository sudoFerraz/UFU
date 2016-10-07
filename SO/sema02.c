#include <unistd.h>     /* Symbolic Constants */
#include <sys/types.h>  /* Primitive System Data Types */ 
#include <errno.h>      /* Errors */
#include <stdio.h>      /* Input/Output */
#include <stdlib.h>     /* General Utilities */
#include <pthread.h>    /* POSIX Threads */
#include <string.h>     /* String handling */
#include <semaphore.h>  /* Semaphore */

/* prototype for thread routine */
void handler ( void *ptr );

/* global vars */
/* semaphores are declared global so they can be accessed 
   in main() and in thread routine,
   here, the semaphore is used as a mutex */
sem_t mutex;
int counter; /* shared variable */

int main()
{
    int i[10], j; /* argument to threads */
    pthread_t threads[10];
    pthread_t thread_b;
    
    
    sem_init(&mutex, 0, 1);      /* initialize mutex to 1 - binary semaphore */
                                 /* second param = 0 - semaphore is local */
                                 
    /* Note: you can check if thread has been successfully created by checking return value of
       pthread_create */             
    do{                         
       counter=0;   
       for(j=0;j<10;j++)
       {    i[j]=j;
           pthread_create (&threads[j], NULL, (void *) &handler, (void *) &i[j]);
       }
    
       for(j=0;j<10;j++)
           pthread_join(threads[j], NULL);

       printf("New Counter Value: %d\n", counter);              
    }while(counter==10);   
    
    sem_destroy(&mutex); /* destroy semaphore */
    exit(0);
} /* main() */

void handler ( void *ptr )
{
    int x, i; 
    x = *((int *) ptr);
    sem_wait(&mutex);
    		 counter=counter+1;
    sem_post(&mutex);
    pthread_exit(0); /* exit thread */
}

