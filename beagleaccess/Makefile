# Changeable settings
LIBNAME :=   beagleaccess

SRCFLDRS :=  src
CSRCFLDRS := src/c
INCFLDRS :=  include
CINCFLDRS := include/c

CPPC :=      g++
CC :=        gcc
CPPFLAGS :=  -g -Wall -std=c++17
CFLAGS :=    -g -Wall

# Auto-gen settings
SRC :=       $(foreach folder,$(SRCFLDRS),$(wildcard $(folder)/*.cpp))
CSRC :=      $(foreach folder,$(CSRCFLDRS),$(wildcard $(folder)/*.c))
INC :=       $(addprefix -I,$(INCFLDRS)) $(addprefix -I,$(CINCFLDRS))
OBJS :=      $(foreach file,$(SRC),obj/$(notdir $(basename $(file))).o)
COBJS :=     $(foreach file,$(CSRC),obj/$(notdir $(basename $(file))).o)

define make-cpp-obj-target
obj/$(notdir $(basename $1)).o : $1
	mkdir -p obj
	$(CPPC) $(INC) $(CPPFLAGS) -c $1 -o obj/$(notdir $(basename $1)).o
endef

define make-c-obj-target
obj/$(notdir $(basename $1)).o : $1
	mkdir -p obj
	$(CC) $(INC) $(CFLAGS) -c $(file) -o obj/$(notdir $(basename $(file))).o
endef

# Build targets
lib$(LIBNAME).a : $(OBJS) $(COBJS)
	mkdir -p obj
	ar rcs lib$(LIBNAME).a $(OBJS) $(COBJS)

$(foreach file,$(SRC),$(eval $(call make-cpp-obj-target,$(file))))
$(foreach file,$(CSRC),$(eval $(call make-c-obj-target,$(file))))

test-access : lib$(LIBNAME).a src/test/TestMain.cpp
	$(CPPC) $(INC) -L. $(CPPFLAGS) -o test-access src/test/TestMain.cpp -l$(LIBNAME)

.PHONY : all
all : lib$(LIBNAME).a test-access

.PHONY : clean
clean :
	rm -rf lib$(LIBNAME).a
	rm -rf obj/
	rm -rf test-access
