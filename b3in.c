//第一个
int main(int argc, char* argv[]) 
{ 
unsigned short total = strlen(argv[1]) + strlen(argv[2]) + 1; 
char* buffer = (char*)malloc(total); 
strcpy(buffer, argv[1]); 
strcat(buffer, argv[2]); 
free(buffer); 
return 0; 
}
//第二个
void CopyIntArray(int *array,int len)
{
	int* myarray,i;
	myarray = malloc(len*sizeof(int));
	if(myarray == NULL)
		return;
	for(i=0;i<len;i++)
		myarray[i] = arrary[i];
}
