#include <signal.h>
#include <stdio.h>

main()
{
	kill(2207,SIGSTOP);
	sleep(5);
	kill(2207,SIGCONT);

} 
