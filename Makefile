
SPIXELS_DIR=./spixels

SPIXELS_LIBRARY=$(SPIXELS_DIR)/lib/libspixels.a

# Configure compiler and libraries:
CXX = g++
CXXFLAGS = -Wall -std=c++11 -O3 -I. -I/opt/vc/include -I/opt/vc/include/interface/vcos/pthreads -I/opt/vc/include/interface/vmcs_host -I/opt/vc/include/interface/vmcs_host/linux -L/opt/vc/lib -I$(SPIXELS_DIR)/include
LIBS = -lrt -lm -lpthread -lbcm_host -L$(SPIXELS_DIR)/lib

# Makefile rules:

capture-test : capture-test.cc
	$(CXX) -o $@ $^ $(CXXFLAGS) $(LIBS)

$(SPIXELS_LIBRARY):
	$(MAKE)  -C $(SPIXELS_DIR)/lib

rpi-fb-matrix: rpi-fb-matrix.o GridTransformer.o Config.o ./rpi-rgb-led-matrix/lib/librgbmatrix.a
	$(CXX) -o $@ $^ $(CXXFLAGS) $(LIBS)

display-test: display-test.o GridTransformer.o Config.o glcdfont.o ./rpi-rgb-led-matrix/lib/librgbmatrix.a
	$(CXX) -o $@ $^ $(CXXFLAGS) $(LIBS)

%.o: %.cpp $(DEPS)
	$(CXX) -c -o $@ $< $(CXXFLAGS)

./rpi-rgb-led-matrix/lib/librgbmatrix.a:
	$(MAKE) -C ./rpi-rgb-led-matrix/lib

.PHONY: clean

clean:
	rm -f *.o rpi-fb-matrix display-test
	$(MAKE) -C ./rpi-rgb-led-matrix/lib clean
