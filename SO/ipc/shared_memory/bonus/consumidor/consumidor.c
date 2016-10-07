#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <sys/shm.h>
#include <semaphore.h>

#define MEM_SZ 4096
#define BUFF_SZ MEM_SZ-sizeof(int)

struct shared_area{	
	char buffer[BUFF_SZ];
	sem_t mutex
}


main()
{
  	int i;
	key_t key=1234;
	struct shared_area *shared_area_ptr;
	void *shared_memory = (void *)0;
	int shmid;

	shmid = shmget(key,MEM_SZ,0666|IPC_CREAT);
	if ( shmid == -1 )
	{
		printf("shmget falhou\n");
		exit(-1);
	}
	
	printf("shmid=%d\n",shmid);
	
	shared_memory = shmat(shmid,(void*)0,0);
	
	if (shared_memory == (void *) -1 )
	{
		printf("shmat falhou\n");
		exit(-1);
	}
		
	printf("Memoria compartilhada no endereco=%x\n",(int)shared_memory);

	shared_area_ptr = (struct shared_area *) shared_memory;

	sem_init(&(shared_area_ptr->mutex))
	for(i=0;i<BUFF_SZ;i++)
		shared_area_ptr->buffer[i]=0;
	
	for(;;)
	{
			sem_wait(&(shared_area_ptr->mutex));
				for(i=0;i<BUFF_SZ;i++)
					printf("%c",shared_area_ptr->buffer[i]);
				printf("\nConsumiu %d bytes\n",i); 
			sem_post(&(shared_area_ptr->mutex));
	}
	sem_destroy(&(shared_area_ptr->mutex));
        exit(0);
}


	
	
