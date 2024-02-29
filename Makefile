CXX = $(CROSS_COMPILE)g++

SAI_PREFIX = /usr
SAI_HEADER_DIR ?= $(SAI_PREFIX)/include/sai
SAI_HEADERS = $(SAI_HEADER_DIR)/sai*.h
CFLAGS = -I$(SAI_HEADER_DIR) -I. -I$(SAI_HEADER_DIR)/experimental -std=c++11
CFLAGS += -O0 -ggdb -Wall -pedantic

DEPS =  switch_sai_rpc.h  switch_sai_types.h
OBJS =  switch_sai_rpc.o  switch_sai_types.o

ODIR = ./src/obj
SAIDIR = ./include
SRC = ./src
THRIFT = /usr/bin/thrift
ifneq (, $(wildcard /usr/local/bin/ctypesgen))
CTYPESGEN = /usr/local/bin/ctypesgen
else
CTYPESGEN = /usr/local/bin/ctypesgen.py
endif
LIBS = -lthrift -lpthread -lsai
SAI_LIBRARY_DIR ?= $(SAI_PREFIX)/lib
LDFLAGS = -L$(SAI_LIBRARY_DIR) -Wl,-rpath=$(SAI_LIBRARY_DIR)
CPP_SOURCES = \
				src/gen-cpp/switch_sai_rpc.cpp \
				src/gen-cpp/switch_sai_rpc.h \
				src/gen-cpp/switch_sai_types.cpp \
				src/gen-cpp/switch_sai_types.h
PY_SOURCES = src/gen-py/switch_sai/switch_sai_rpc.py

MKDIR_P = mkdir -p

all: directories $(ODIR)/librpcserver.a saiserver

directories:
	$(MKDIR_P) $(ODIR)

$(CPP_SOURCES): src/switch_sai.thrift
	\rm -fr $(SRC)/gen-cpp
	$(THRIFT) -o $(SRC) --gen cpp -r $(SRC)/switch_sai.thrift

$(PY_SOURCES): src/switch_sai.thrift
	\rm -fr $(SRC)/gen-py
	$(THRIFT) -o $(SRC) --gen py -r $(SRC)/switch_sai.thrift

$(ODIR)/%.o: src/gen-cpp/%.cpp
	$(CXX) $(CFLAGS) -c $^ -o $@

$(ODIR)/switch_sai_rpc_server.o: src/switch_sai_rpc_server.cpp
	$(CXX) $(CFLAGS) -c $^ -o $@ $(CFLAGS) -I$(SRC)/gen-cpp

$(ODIR)/saiserver.o: src/saiserver.cpp
	$(CXX) $(CFLAGS) -c $^ -o $@ $(CFLAGS) $(CDEFS) -I$(SRC)/gen-cpp -I$(SRC)

$(ODIR)/librpcserver.a: $(ODIR)/switch_sai_rpc.o $(ODIR)/switch_sai_types.o $(ODIR)/switch_sai_rpc_server.o $(CONSTANS_OBJ)
	ar rcs $(ODIR)/librpcserver.a $(ODIR)/switch_sai_rpc.o $(ODIR)/switch_sai_types.o  $(ODIR)/switch_sai_rpc_server.o $(CONSTANS_OBJ)

saiserver: $(ODIR)/saiserver.o $(ODIR)/librpcserver.a
	$(CXX) $(LDFLAGS) $(ODIR)/switch_sai_rpc_server.o $(ODIR)/saiserver.o -o $@ \
		   $(ODIR)/librpcserver.a $(LIBS)

clean:
	rm -rf $(ODIR) $(SRC)/gen-* saiserver dist
