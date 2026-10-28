CXX = $(CROSS_COMPILE)g++

SAI_PREFIX ?= /usr
SAI_HEADER_DIR ?= $(SAI_PREFIX)/include/sai
SAI_LIBRARY_DIR ?= $(SAI_PREFIX)/lib
CFLAGS = -I$(SAI_HEADER_DIR) -I$(SAI_HEADER_DIR)/experimental -I$(SAI_HEADER_DIR)/../experimental -I. -Isrc -Isrc/gen-cpp -std=c++11
CFLAGS += -O0 -ggdb -Wall -pedantic
LIBS = -lthrift -lpthread -ldl
LDFLAGS += -L$(SAI_LIBRARY_DIR) -Wl,-rpath=$(SAI_LIBRARY_DIR)

ODIR = ./src/obj
SRC = ./src
THRIFT ?= thrift
IDL = idl/switch_sai.thrift idl/sai_tui.thrift
CPP_SOURCES = src/gen-cpp/switch_sai_rpc.cpp src/gen-cpp/switch_sai_types.cpp \
              src/gen-cpp/SaiTui.cpp src/gen-cpp/sai_tui_types.cpp
CPP_HEADERS = $(CPP_SOURCES:.cpp=.h)
PY_SOURCES = src/gen-py/switch_sai/switch_sai_rpc.py src/gen-py/sai_tui/SaiTui.py
RPC_OBJS = $(ODIR)/switch_sai_rpc.o $(ODIR)/switch_sai_types.o \
           $(ODIR)/SaiTui.o $(ODIR)/sai_tui_types.o \
           $(ODIR)/switch_sai_rpc_server.o $(ODIR)/tui_rpc.o $(ODIR)/interface_address.o

.PHONY: all directories clean test-server
all: $(ODIR)/librpcserver.a saiserver $(PY_SOURCES)
directories: $(ODIR)
$(ODIR):
	mkdir -p $@

# Grouped targets (GNU make >= 4.3) prevent parallel recursive codegen races.
# Both IDLs invalidate both language outputs; a deleted output is regenerated.
$(CPP_SOURCES) $(CPP_HEADERS) &: $(IDL)
	$(THRIFT) -o $(SRC) --gen cpp -r idl/switch_sai.thrift
$(PY_SOURCES) &: $(IDL)
	$(THRIFT) -o $(SRC) --gen py -r idl/switch_sai.thrift

$(ODIR)/%.o: src/gen-cpp/%.cpp $(CPP_HEADERS) | $(ODIR)
	$(CXX) $(CPPFLAGS) $(CFLAGS) $(CXXFLAGS) -MMD -MP -c $< -o $@
$(ODIR)/switch_sai_rpc_server.o: src/switch_sai_rpc_server.cpp src/tui_rpc.h $(CPP_HEADERS) | $(ODIR)
	$(CXX) $(CPPFLAGS) $(CFLAGS) $(CXXFLAGS) -MMD -MP -c $< -o $@
$(ODIR)/tui_rpc.o: src/tui_rpc.cpp src/tui_rpc.h $(CPP_HEADERS) | $(ODIR)
	$(CXX) $(CPPFLAGS) $(CFLAGS) $(CXXFLAGS) -MMD -MP -c $< -o $@
$(ODIR)/saiserver.o: src/saiserver.cpp $(CPP_HEADERS) | $(ODIR)
	$(CXX) $(CPPFLAGS) $(CFLAGS) $(CXXFLAGS) $(CDEFS) -MMD -MP -c $< -o $@
$(ODIR)/notifications.o: src/notifications.cpp src/notifications.h | $(ODIR)
	$(CXX) $(CPPFLAGS) $(CFLAGS) $(CXXFLAGS) -MMD -MP -c $< -o $@

$(ODIR)/interface_address.o: src/interface_address.cpp src/interface_address.h | $(ODIR)
	$(CXX) $(CPPFLAGS) $(CFLAGS) $(CXXFLAGS) -pthread -MMD -MP -c $< -o $@
$(ODIR)/sai_dynamic.o: src/sai_dynamic.cpp | $(ODIR)
	$(CXX) $(CPPFLAGS) $(CFLAGS) $(CXXFLAGS) -MMD -MP -c $< -o $@

$(ODIR)/librpcserver.a: $(RPC_OBJS) $(CONSTANS_OBJ)
	ar rcs $@ $^
saiserver: $(ODIR)/saiserver.o $(ODIR)/notifications.o $(ODIR)/librpcserver.a $(ODIR)/sai_dynamic.o
	$(CXX) $(LDFLAGS) -o $@ $^ $(LIBS)

test-server:
	SAI_HEADER_DIR="$(SAI_HEADER_DIR)" THRIFT="$(THRIFT)" CXX="$(CXX)" tests/server/run.sh
	SAI_HEADER_DIR="$(SAI_HEADER_DIR)" CXX="$(CXX)" tests/server/interface_address_run.sh
	SAI_HEADER_DIR="$(SAI_HEADER_DIR)" CXX="$(CXX)" tests/server/dynamic_run.sh

-include $(wildcard $(ODIR)/*.d)
clean:
	rm -rf $(ODIR) $(SRC)/gen-* saiserver dist
