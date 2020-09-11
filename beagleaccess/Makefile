# Changeable settings
LIBNAME :=   beagleaccess

SRCFLDRS :=  src
CSRCFLDRS := src/c
INCFLDRS :=  include
CINCFLDRS := include/c

CPPC :=      g++
CC :=        gcc
CPPFLAGS :=  -O2 -Wall -std=c++17
CFLAGS :=    -O2 -Wall

# Auto-gen settings
SRC :=       $(foreach folder,$(SRCFLDRS),$(wildcard $(folder)/*.cpp))
CSRC :=      $(foreach folder,$(CSRCFLDRS),$(wildcard $(folder)/*.c))
HFILES :=    $(foreach folder,$(INCFLDRS),$(wildcard $(folder)/*.hpp))
CHFILES :=   $(foreach folder,$(CINCFLDRS),$(wildcard $(folder)/*.h))
INC :=       $(addprefix -I,$(INCFLDRS)) $(addprefix -I,$(CINCFLDRS))
OBJS :=      $(foreach file,$(SRC),obj/$(notdir $(basename $(file))).o) $(foreach file,$(CSRC),obj/$(notdir $(basename $(file))).o)

# Build targets
lib$(LIBNAME).a : $(SRC) $(HFILES) $(CSRC) $(CHFILES)
	mkdir -p obj
	$(foreach file,$(SRC),\
		$(CPPC) $(INC) $(CPPFLAGS) -c $(file) -o obj/$(notdir $(basename $(file))).o;\
	)
	$(foreach file,$(CSRC),\
		$(CC) $(INC) $(CFLAGS) -c $(file) -o obj/$(notdir $(basename $(file))).o;\
	)
	ar rcs lib$(LIBNAME).a $(OBJS)

test-access : lib$(LIBNAME).a src/test/TestMain.cpp
	$(CPPC) $(INC) -L. $(CPPFLAGS) -o test-access src/test/TestMain.cpp -l$(LIBNAME)

.PHONY : all
all : lib$(LIBNAME).a test-access

.PHONY : clean
clean :
	rm -rf lib$(LIBNAME).a
	rm -rf obj/
	rm -rf test-access
