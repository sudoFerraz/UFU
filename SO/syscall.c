main(){
	char buffer;
	int i;
	i = read(0,&buffer,1);
	while(i>0){
		write(1,&buffer,1);
		i = read(0,&buffer,1);
	}
}
