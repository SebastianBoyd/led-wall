import ctypes
import os
libtest=ctypes.cdll.LoadLibrary("./library.so")
output=libtest.main()
print output
