// Research only: compose the verified TLS getter contract with request control.
// No loader, addresses, TLS setter, scheduler, or implicit native cancellation.
#pragma once
#include "newsendmsg_operation_4115.hpp"

namespace newsendmsg4115 {
struct ExecutorContext {
  // Frozen getter ABI: no arguments, returns the current executor raw base.
  // The caller must separately prove expected_executor and its lifetime.
  void* (*current_executor)();
  void* expected_executor;
};

class ExecutorResearchOperation {
 public:
  using Clock = ResearchOperation::Clock;
  ExecutorResearchOperation(ExecutorContext context, OperationFunctions functions,
                            void* service, const void* options,
                            const std::string& routing, const void* body,
                            std::size_t size, Clock::time_point deadline)
      : context_(context),
        operation_(checked_functions(context_, functions), service, options,
                   routing, body, size, deadline) {}
  ExecutorResearchOperation(const ExecutorResearchOperation&) = delete;
  ExecutorResearchOperation& operator=(const ExecutorResearchOperation&) = delete;
  ExecutorResearchOperation(ExecutorResearchOperation&&) = delete;
  ExecutorResearchOperation& operator=(ExecutorResearchOperation&&) = delete;
  ~ExecutorResearchOperation() = default;

  bool cancel() {
    require_executor(context_);
    return operation_.cancel(); // Retains the independent thread-lifetime token.
  }
  bool expire(Clock::time_point now) {
    require_executor(context_); // Also check early and already-terminal commands.
    return operation_.expire(now);
  }
  OperationSnapshot snapshot() const { return operation_.snapshot(); }
  std::uint32_t task_id() const noexcept { return operation_.task_id(); }

 private:
  static void require_executor(const ExecutorContext& context) {
    if (!context.current_executor || !context.expected_executor)
      throw std::invalid_argument("executor getter and expected identity required");
    if (context.current_executor() != context.expected_executor)
      throw std::logic_error("operation requires its proven executor context");
  }
  static OperationFunctions checked_functions(const ExecutorContext& context,
                                               OperationFunctions functions) {
    require_executor(context); // Runs before NativeBody construction or factory.
    return functions;
  }
  const ExecutorContext context_;
  ResearchOperation operation_;
};
} // namespace newsendmsg4115
