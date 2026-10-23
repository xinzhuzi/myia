// Research ABI for a frozen native service return; no loader or execution route.
#pragma once
#include "newsendmsg_text_input_4115.hpp"
#include <type_traits>

namespace newsendmsg4115 {
struct TextServiceValueOpaque;
struct TextServiceResult {
  // Selected consumer tests these two words independently for zero.
  std::uint32_t status_first = 0;
  std::uint32_t status_second = 0;
  std::string status_text;
  std::shared_ptr<TextServiceValueOpaque> value;
};
// 0x317ded4: x0=service, x1=input shared pair address; nontrivial x8 result.
// Its forwarding callee waits inside 0x3189980. A plain executor stack is not
// sufficient. Actual coroutine/service lifetime and final drain are unproved.
using SubmitTextInput = TextServiceResult (*)(void*, const TextInputHandle*);
static_assert(std::is_standard_layout_v<TextServiceResult>);
static_assert(offsetof(TextServiceResult, status_first) == 0);
static_assert(offsetof(TextServiceResult, status_second) == 4);
static_assert(offsetof(TextServiceResult, status_text) == 8);
static_assert(offsetof(TextServiceResult, value) == 0x20);
static_assert(sizeof(TextServiceResult) == 0x30 && alignof(TextServiceResult) == 8);
static_assert(!std::is_trivially_destructible_v<TextServiceResult>);
} // namespace newsendmsg4115
