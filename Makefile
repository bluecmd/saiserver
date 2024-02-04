CXX = $(CROSS_COMPILE)g++

SAI_PREFIX = /usr
SAI_HEADER_DIR ?= $(SAI_PREFIX)/include/sai
SAI_HEADERS = $(SAI_HEADER_DIR)/sai*.h
CFLAGS = -I$(SAI_HEADER_DIR) -I. -I$(SAI_HEADER_DIR)/experimental -std=c++11
ifeq ($(DEBUG),1)
CFLAGS += -O0 -ggdb
endif

# Detect THRIFT_VERSION
THRIFT_VERSION = $(shell thrift  -version | cut -d ' ' -f3)
ifeq ($(shell dpkg --compare-versions $(THRIFT_VERSION) "le" 0.11.0 && echo True), True)
CFLAGS += -DFORCE_BOOST_SMART_PTR
endif

ifeq ($(platform),MLNX)
CDEFS = -DMLNXSAI
else
ifeq ($(platform),BFT)
CDEFS = -DBFTSAI
else
ifeq ($(platform),CAVIUM)
CDEFS = -DCAVIUMSAI
else
CDEFS = -DBRCMSAI
endif
endif
endif
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
LIBS = -lthrift -lpthread
ifeq ($(platform),vs)
LIBS += -lsaivs -lsaimeta -lsaimetadata -lzmq
else
LIBS += -lsai
endif
SAI_LIBRARY_DIR ?= $(SAI_PREFIX)/lib
LDFLAGS = -L$(SAI_LIBRARY_DIR) -Wl,-rpath=$(SAI_LIBRARY_DIR)
CPP_SOURCES = \
				src/gen-cpp/switch_sai_rpc.cpp \
				src/gen-cpp/switch_sai_rpc.h \
				src/gen-cpp/switch_sai_types.cpp \
				src/gen-cpp/switch_sai_types.h

MKDIR_P = mkdir -p
INSTALL := /usr/bin/install

ifeq ($(shell dpkg --compare-versions $(THRIFT_VERSION) "lt" 0.14.1 && echo True), True)
DEPS += switch_sai_constants.h
OBJS += switch_sai_constants.o
CPP_SOURCES += src/gen-cpp/switch_sai_constants.cpp \
               src/gen-cpp/switch_sai_constants.h

CONSTANS_OBJ = $(ODIR)/switch_sai_constants.o
endif

all: directories $(ODIR)/librpcserver.a saiserver

directories:
	$(MKDIR_P) $(ODIR)

$(CPP_SOURCES): src/switch_sai.thrift
	$(THRIFT) -o $(SRC) --gen cpp -r $(SRC)/switch_sai.thrift

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
	rm -rf $(ODIR) $(SRC)/gen-cpp saiserver dist
