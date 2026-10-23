// Research component for the frozen 4.1.15 input contract. No loader or send.
#pragma once
#include <cstddef>
#include <cstdint>
#include <cstring>
#include <memory>
#include <stdexcept>
#include <string>

namespace newsendmsg4115 {
struct TextInputOpaque;
using TextInputHandle = std::shared_ptr<TextInputOpaque>;
using CreateTextInput = TextInputHandle (*)(); // Nontrivial return via hidden x8.
using AssignInputString = std::string& (*)(std::string&, const std::string&);

struct TextInputFunctions {
  CreateTextInput create;
  AssignInputString assign;
  const void* expected_vtable; // Identity/lifetime must be proven by the caller.
};

class NativeTextInput {
 public:
  NativeTextInput(TextInputFunctions functions, const std::string& chat_id,
                  const std::string& content) {
    if (!functions.create || !functions.assign || !functions.expected_vtable)
      throw std::invalid_argument("text input functions and proven identity required");
    if (chat_id.empty() || content.empty())
      throw std::invalid_argument("chat_id and content must be nonempty");
    // Own the factory result before any operation which can throw.
    handle_ = functions.create();
    if (!handle_ || handle_.use_count() == 0)
      throw std::runtime_error("text input factory returned no owned payload");
    auto* payload = reinterpret_cast<std::byte*>(handle_.get());
    const void* actual_vtable;
    std::memcpy(&actual_vtable, payload, sizeof(actual_vtable));
    if (actual_vtable != functions.expected_vtable)
      throw std::runtime_error("text input factory identity mismatch");
    std::uint32_t low, high;
    std::memcpy(&low, payload + 0xe4, sizeof(low));
    std::memcpy(&high, payload + 0xe8, sizeof(high));
    if (low != 0 || high != 0)
      throw std::runtime_error("text input must have fresh numeric type fields");
    auto& routing = *reinterpret_cast<std::string*>(payload + 0x90);
    auto& body = *reinterpret_cast<std::string*>(payload + 0x5c8);
    if (!routing.empty() || !body.empty())
      throw std::runtime_error("text input must have fresh string fields");
    functions.assign(routing, chat_id);
    functions.assign(body, content);
    // Match the native numeric-one builder; publish readiness only on success.
    low = 1;
    std::memcpy(payload + 0xe4, &low, sizeof(low));
  }
  NativeTextInput(const NativeTextInput&) = delete;
  NativeTextInput& operator=(const NativeTextInput&) = delete;
  NativeTextInput(NativeTextInput&&) = delete;
  NativeTextInput& operator=(NativeTextInput&&) = delete;
  ~NativeTextInput() = default;

  // A consumer must independently prove service ABI, coroutine and lifetime.
  const TextInputHandle& handle() const noexcept { return handle_; }

 private:
  TextInputHandle handle_;
};

static_assert(sizeof(TextInputHandle) == 16 && alignof(TextInputHandle) == 8);
static_assert(sizeof(std::string) == 24 && alignof(std::string) == 8);
static_assert(sizeof(void*) == 8);
} // namespace newsendmsg4115
