# Project settings
OBJNAME :=  measure
SRCFLDRS := src
INCFLDRS := 
CC :=       gcc
CFLAGS :=   -O2 -Wall

# Auto gen settings
SRC :=      $(foreach folder, $(SRCFLDRS), $(wildcard $(folder)/*.c))
HFILES :=   $(foreach folder, $(INCFLDRS), $(wildcard $(folder)/*.h))
INC :=      $(addprefix -I,$(INCFLDRS))

# Build targets
$(OBJNAME) : $(SRC) $(HFILES)
	$(CC) $(INC) $(CFLAGS) -o $(OBJNAME) $(SRC)
	chmod +x $(OBJNAME)

.PHONY : clean
clean :
	rm -rf $(OBJNAME)