#include <unistd.h>
int main() { return write(2, "main reached\n", 13) == 13 ? 0 : 1; }
