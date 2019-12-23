#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>

int main(void) {

	char buf[32];

	fgets(buf, 64, stdin);

	if (1 == 2) {
		return 0;
	}

	if (strncmp(buf, "hello there", strlen("hello there"))) {
		exit(1);
	}

	return 0;
}
