#include <functional>
#include <iostream>
#include <string>
int main() {
  std::cout << "{\"function_size\":" << sizeof(std::function<bool(void*,int,int)>)
            << ",\"function_alignment\":" << alignof(std::function<bool(void*,int,int)>)
            << ",\"string_size\":" << sizeof(std::string)
            << ",\"string_alignment\":" << alignof(std::string) << "}\n";
}
