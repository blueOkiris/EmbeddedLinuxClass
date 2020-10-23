# Build options
OBJNAME := app.arm
CC :=      gcc
CFLAGS :=  -Iinclude \
           -O2 -Wall -Werror
LD :=      gcc
LDFLAGS := 
SRCDIR :=  src
OBJDIR :=  obj

# Auto generate some options like files
SRC :=     $(wildcard $(SRCDIR)/*.c)
OBJS :=    $(subst src,$(OBJDIR),$(subst .c,.o,$(SRC)))

# Generic targets
.PHONY : all
all : $(OBJNAME)

.PHONY : clean
clean :
	rm -rf $(OBJNAME)
	rm -rf $(OBJDIR)

$(OBJDIR)/%.o : $(SRCDIR)/%.c
	mkdir -p obj
	$(CC) $(CFLAGS) -c $< -o $@

# "Real" build targets
$(OBJNAME) : $(OBJS)
	$(LD) $(LDFLAGS) $(OBJS) -o $@