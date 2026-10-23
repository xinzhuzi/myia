// Disposable synthetic native layout; never loads or contacts WeChat.
#include <array>
#include <cstddef>
#include <cstdint>
#include <string>
#include <unistd.h>

constexpr std::uintptr_t base = 0x100000000;
struct Wrapper { std::uintptr_t vtable; const std::string* value; std::uint32_t cached, mask; };
struct Item {
    std::uintptr_t vtable; Wrapper* wrapper; const std::string* content;
    std::uint32_t type, time; const std::string* source;
    std::uint32_t client, field7, cached, mask;
};
struct Body {
    std::uintptr_t vtable; Item** items;
    std::int32_t count, allocated, capacity, padding;
    std::uint32_t declared, unused, mask, cached;
};
static_assert(sizeof(std::string) == 24 && sizeof(Wrapper) == 24);
static_assert(sizeof(Item) == 56 && offsetof(Item, mask) == 52);
static_assert(sizeof(Body) == 48 && offsetof(Body, count) == 16);
extern "C" __attribute__((noinline)) void fixture_factory(void* service, Body* body, const std::string* text) {
    asm volatile("" : : "r"(service), "r"(body), "r"(text) : "memory");
}
int main() {
    const std::string recipient = "filehelper", content = "fixture synthetic message", source, context;
    Wrapper wrapper{base + 0x9eca390, &recipient, 0, 1};
    Item item{base + 0x9e91d80, &wrapper, &content, 1, 1700000000, &source, 12345, 0, 0, 0x1f};
    Item* items[] = {&item};
    Body body{base + 0x9e91df8, items, 1, 1, 1, 0, 1, 0, 1, 0};
    for (int i = 0; i < 80; ++i) {
        fixture_factory(reinterpret_cast<void*>(0x200000000), &body, &context);
        usleep(100000);
    }
}
