// Owned host-only regression: no target process or native scheduler.
#include "newsendmsg_body_start_gate_4115.hpp"
#include <iostream>
using namespace newsendmsg4115;
int main() {
  std::shared_ptr<BodyStartGate> admission, cancellation;
  std::thread::id original;
  std::thread owner([&] {
    original = std::this_thread::get_id();
    admission = std::make_shared<BodyStartGate>();
    cancellation = std::make_shared<BodyStartGate>();
  });
  owner.join();
  int reused = 0, rejected = 0, native_calls = 0;
  for (int i = 0; i < 64; ++i) {
    std::thread replacement([&] {
      if (std::this_thread::get_id() == original) ++reused;
      if (admission->admit() == BodyAdmission::reject) ++rejected;
      if (cancellation->cancel_on_executor([&] { ++native_calls; }) ==
          JobCancelAction::wrong_executor) ++rejected;
    });
    replacement.join();
  }
  const auto body = admission->snapshot(), cancel = cancellation->snapshot();
  const bool passed = rejected == 128 && native_calls == 0 &&
      !body.invoked && !body.entered && body.wrong_executor &&
      !cancel.cancel_requested && cancel.wrong_executor;
  std::cout << "{\"passed\":" << (passed ? "true" : "false")
            << ",\"replacement_threads\":64,\"reused_thread_ids\":" << reused
            << ",\"rejected_entries\":" << rejected
            << ",\"native_calls\":" << native_calls
            << ",\"target_executed\":false,\"sent\":false}\n";
  return passed ? 0 : 1;
}
