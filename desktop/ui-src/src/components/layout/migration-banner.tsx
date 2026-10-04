import { ArrowRight, Info, X } from "lucide-react";
import { useEffect, useRef, useState } from "react";
import { useNavigate } from "react-router-dom";

import { Button } from "@/components/ui/button";
import { pyenvMigrationBanner } from "@/screens/settings/pyenv-api";

/**
 * 存量迁移一次性引导横幅(10-05-desktop-managed-py-env 第 6 步,D5/design §6)。
 *
 * 新版首启检测到旧数据根(壳侧判:旧痕迹在 && python-env.json 不在 && 未引导
 * 过)→ 本横幅出现:告知「新版改为自管 Python 环境,需一次性配置」并引导进
 * 设置。**数据零迁移**(db/plugins/models/keychain 原样沿用)—— 横幅只跳
 * 设置,绝不改数据;唯一落盘 = 壳侧引导标记。
 *
 * 一次性语义:命令 `pyenv_migration_banner` 查询即消费(壳侧标记落盘,同一
 * 数据根上 show=true 至多一次,含重启)。本组件挂载时只查一次(ref 防御
 * StrictMode 双效应),关闭/跳转仅隐藏本会话的横幅,不复现不重查。
 * 查询失败(浏览器直开/致命盘况)→ 静默不渲染:横幅是辅助引导,环境态的
 * 真相源在设置屏 PyenvCard(pyenv_get_status 有 ErrorBox 大声报错)。
 */
export function MigrationBanner() {
  const [visible, setVisible] = useState(false);
  /** 挂载效应只跑一次查询(StrictMode 双效应/重挂载不再消费壳侧一次性) */
  const queried = useRef(false);
  const navigate = useNavigate();

  useEffect(() => {
    if (queried.current) return;
    queried.current = true;
    // 不设 cancelled:StrictMode 双效应 = run1 查询 → cleanup → run2 被 ref
    // 挡住,若 run1 的结果按「已清理」丢弃,唯一一次查询就被浪费了(横幅
    // 永不出现);让结果落在仍存活的实例上,真卸载后的 setVisible 在
    // React 18+ 是无告警 no-op,无须防御。
    pyenvMigrationBanner()
      .then((decision) => {
        // 只翻向出现:晚到的 false 决不撤销已出现的引导(双效应竞态防御)
        if (decision.show) setVisible(true);
      })
      .catch((error: unknown) => {
        // 辅助引导不拦主界面:失败静默(console 留排查线索,真相源在设置屏)
        console.error("migration-banner: 查询存量迁移引导失败", error);
      });
  }, []);

  if (!visible) return null;

  const gotoSettings = () => {
    setVisible(false); // 跳设置即卸载横幅(配置动作在设置页接手)
    navigate("/settings?section=python-env");
  };

  return (
    <div
      data-testid="migration-banner"
      role="status"
      className="flex items-start gap-3 border-b border-border/60 bg-muted/40 px-4 py-3"
    >
      <Info className="mt-0.5 size-4 shrink-0 text-warning" />
      <div className="min-w-0 flex-1">
        <p className="text-sm font-medium text-foreground">检测到旧版数据:新版改为自管 Python 环境,需一次性配置</p>
        <p className="mt-1 text-xs leading-5 text-muted-foreground">
          你的数据库、插件、模型与钥匙串凭据全部原样沿用,零迁移零丢失;首次使用前请在设置的「Python 环境」分区完成一次配置(运行时与依赖在线下载,首跑需联网)。
        </p>
      </div>
      <div className="flex shrink-0 items-center gap-1.5">
        <Button
          size="sm"
          onClick={gotoSettings}
          data-testid="migration-banner-goto-settings"
          title="跳转设置 → Python 环境(开始配置)"
        >
          前往设置
          <ArrowRight className="size-3.5" />
        </Button>
        <Button
          size="icon"
          variant="ghost"
          onClick={() => setVisible(false)}
          data-testid="migration-banner-close"
          aria-label="关闭引导(本次会话内不再显示)"
          title="关闭引导(本次会话内不再显示)"
        >
          <X className="size-4" />
        </Button>
      </div>
    </div>
  );
}
