
SPIXELS_DIR=./spixels

SPIXELS_LIBRARY=$(SPIXELS_DIR)/lib/libspixels.a

# Configure compiler and libraries:
CXX = g++
CXXFLAGS = -Wall -std=c++11 -O3 -I. -I/opt/vc/include -I/opt/vc/include/interface/vcos/pthreads -I/opt/vc/include/interface/vmcs_host -I/opt/vc/include/interface/vmcs_host/linux -L/opt/vc/lib -I$(SPIXELS_DIR)/include
CXXFLAGS+=$(shell python-config --cflags)
LIBS = -lrt -lm -lpthread -lbcm_host -L$(SPIXELS_DIR)/lib
LIBS+=$(shell python-config --ldflags)

# Makefile rules:

capture-test : capture-test.cc
	$(CXX) -o $@ $^ $(CXXFLAGS) $(LIBS)

strand : strand.cc wrapper.cc $(SPIXELS_LIBRARY)
	$(CXX) -o $@ $^ $(CXXFLAGS) $(LIBS)
	$(CXX) -shared -c -fPIC $^ $(CXXFLAGS) $(LIBS) -o $@.o
	$(CXX) -shared -o library.so $@.o -Wl,-soname,library.so 

pixel-test : pixel_test.cc $(SPIXELS_LIBRARY)
	$(CXX) -o $@ $^ $(CXXFLAGS) $(LIBS)
	
$(SPIXELS_LIBRARY):
	$(MAKE)  -C $(SPIXELS_DIR)/lib


.PHONY: clean

clean:
	rm -f *.o rpi-fb-matrix display-test
	$(MAKE) -C ./rpi-rgb-led-matrix/lib clean
