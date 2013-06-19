CC	=	gcc
DEST	=	/usr/local/bin
PROGRAM	=	hello


${PROGRAM}:	hello.c
		gcc -o hello hello.c


install:	${PROGRAM}
		install -s ${PROGRAM} ${DEST}

clean:
		rm -f m.o *~ ${PROGRAM}
