# Changeable settings
LIBNAME :=  beagleaccess

SRCFLDRS := src
INCFLDRS := include

CPPC :=     g++
CPPFLAGS := -O2 -Wall -std=c++17

# Auto-gen settings
SRC :=      $(foreach folder,$(SRCFLDRS),$(wildcard $(folder)/*.cpp))
HFILES :=   $(foreach folder,$(INCFLDRS),$(wildcard $(folder)/*.hpp))
INC :=      $(addprefix -I,$(INCFLDRS))
OBJS :=     $(foreach file,$(SRC),obj/$(notdir $(basename $(file))).o)

# Build targets
lib$(LIBNAME).a : $(SRC) $(HFILES)
	mkdir -p obj
	$(foreach file,$(SRC),\
		$(CPPC) $(INC) $(CPPFLAGS) -c $(file) -o obj/$(notdir $(basename $(file))).o;\
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
