#include <iostream>
#include <stdexcept>

#include <bcm_host.h>
#include <fcntl.h>
#include <linux/fb.h>
#include <signal.h>
#include <sys/ioctl.h>
#include <sys/mman.h>
#include <time.h>
#include <unistd.h>

using namespace std;

class BCMDisplayCapture {
public:
  BCMDisplayCapture(int width=-1, int height=-1):
    _width(width),
    _height(height),
    _display(0),
    _screen_resource(0),
    _screen_data(NULL)
  {
    // Get information about primary/HDMI display.
    _display = vc_dispmanx_display_open(0);
    if (!_display) {
      throw runtime_error("Unable to open primary display!");
    }
    DISPMANX_MODEINFO_T display_info;
    if (vc_dispmanx_display_get_info(_display, &display_info)) {
      throw runtime_error("Unable to get primary display information!");
    }
    cout << "Primary display:" << endl
         << " resolution: " << display_info.width << "x" << display_info.height << endl
         << " format: " << display_info.input_format << endl;
    // If no width and height were specified then grab the entire screen.
    if ((_width == -1) || (_height == -1)) {
      _width = display_info.width;
      _height = display_info.height;
    }
    // Create a GPU image surface to hold the captured screen.
    uint32_t image_prt;
    _screen_resource = vc_dispmanx_resource_create(VC_IMAGE_RGB888, _width, _height, &image_prt);
    if (!_screen_resource) {
      throw runtime_error("Unable to create screen surface!");
    }
    // Create a rectangular region of the captured screen size.
    vc_dispmanx_rect_set(&_rect, 0, 0, _width, _height);
    // Allocate CPU memory for copying out the captured screen.  Must be aligned
    // to a larger size because of GPU surface memory size constraints.
    _pitch = ALIGN_UP(_width*3, 32);
    _screen_data = new uint8_t[_pitch*_height];
  }

  void capture() {
    // Capture the primary display and copy it from GPU to CPU memory.
    vc_dispmanx_snapshot(_display, _screen_resource, (DISPMANX_TRANSFORM_T)0);
    vc_dispmanx_resource_read_data(_screen_resource, &_rect, _screen_data, _pitch);
  }

  void getPixel(int x, int y, uint8_t* r, uint8_t* g, uint8_t* b) {
    // Grab the requested pixel from the last captured display image.
    uint8_t* row = _screen_data + (y*_pitch);
    *r = row[x*3];
    *g = row[x*3+1];
    *b = row[x*3+2];
  }

  ~BCMDisplayCapture() {
    // Clean up BCM and other resources.
    if (_screen_resource != 0) {
      vc_dispmanx_resource_delete(_screen_resource);
    }
    if (_display != 0) {
      vc_dispmanx_display_close(_display);
    }
    if (_screen_data != NULL) {
      delete[] _screen_data;
    }
  }

private:
  int _width,
      _height,
      _pitch;
  DISPMANX_DISPLAY_HANDLE_T _display;
  DISPMANX_RESOURCE_HANDLE_T _screen_resource;
  VC_RECT_T _rect;
  uint8_t* _screen_data;
};

int main() {
    bcm_host_init();
    BCMDisplayCapture displayCapture(400, 800);



    // Loop forever waiting for Ctrl-C signal to quit.
    signal(SIGINT, sigintHandler);
    cout << "Press Ctrl-C to quit..." << endl;
    while (running) {
      // Capture the current display image.
      displayCapture.capture();
      // Loop through the frame data and set the pixels on the matrix canvas.
      for (int y=0; y<40; ++y) {
        for (int x=0; x<20; ++x) {
          uint8_t red, green, blue;
          displayCapture.getPixel(x+x_offset, y+y_offset, &red, &green, &blue);
          canvas->SetPixel(x, y, red, green, blue);
        }
      }
      // Sleep for 25 milliseconds (40Hz refresh)
      usleep(25 * 1000);
    }
    delete canvas;
}