import { afterEach, describe, expect, it } from "vitest";

import {
  NOTIFY_ROUTE_SIGNAL,
  setPendingNotifyChannel,
  takePendingNotifyChannel,
} from "./notify-route";

/** 挂起槽契约(10-15 粒度细化:source + itemKey 两元组)。 */
describe("notify-route pending slot", () => {
  afterEach(() => {
    // 挂起槽是模块级单例:每测后清空防串味
    takePendingNotifyChannel();
  });

  it("存取两元组:itemKey 随 source 一起挂起,一次消费后清空", () => {
    setPendingNotifyChannel("tms 群", "dk-latest-1");
    expect(takePendingNotifyChannel()).toEqual({ source: "tms 群", itemKey: "dk-latest-1" });
    expect(takePendingNotifyChannel()).toBeNull();
  });

  it("itemKey 缺席/空白 = 会话级(itemKey: null)", () => {
    setPendingNotifyChannel("tms 群");
    expect(takePendingNotifyChannel()).toEqual({ source: "tms 群", itemKey: null });
    setPendingNotifyChannel("tms 群", "   ");
    expect(takePendingNotifyChannel()).toEqual({ source: "tms 群", itemKey: null });
  });

  it("source 空 = 不存(异常条目只唤不链)", () => {
    setPendingNotifyChannel("", "dk-1");
    expect(takePendingNotifyChannel()).toBeNull();
    setPendingNotifyChannel(null, "dk-1");
    expect(takePendingNotifyChannel()).toBeNull();
  });

  it("信号名契约钉死(壳事件窗口直发面,勿改字面)", () => {
    expect(NOTIFY_ROUTE_SIGNAL).toBe("myia:notify-route");
  });
});
