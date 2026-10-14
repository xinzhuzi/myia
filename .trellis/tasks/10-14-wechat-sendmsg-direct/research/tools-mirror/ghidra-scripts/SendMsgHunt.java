/* ###
 * SendMsgFtouser 定向猎杀:字符串 xref + 已知地址反编译(task 10-14-wechat-sendmsg-direct)
 * @category Analysis
 */
import ghidra.app.decompiler.DecompInterface;
import ghidra.app.decompiler.DecompileOptions;
import ghidra.app.decompiler.DecompileResults;
import ghidra.app.script.GhidraScript;
import ghidra.program.model.address.Address;
import ghidra.program.model.listing.Function;
import ghidra.program.model.listing.Data;
import ghidra.program.model.mem.Memory;
import ghidra.program.model.symbol.Reference;
import ghidra.program.model.symbol.ReferenceIterator;

import java.io.File;
import java.io.FileWriter;
import java.io.PrintWriter;
import java.util.LinkedHashSet;
import java.util.Set;

public class SendMsgHunt extends GhidraScript {

    private PrintWriter out;
    private DecompInterface decompiler;

    private Function decompileAt(long va, String tag) {
        Address a = currentProgram.getAddressFactory().getDefaultAddressSpace().getAddress(va);
        Function f = getFunctionContaining(a);
        if (f == null) {
            out.println("// [" + tag + "] " + Long.toHexString(va) + " 无归属函数");
            return null;
        }
        DecompileResults r = decompiler.decompileFunction(f, 60, monitor);
        out.println("// ===== [" + tag + "] " + f.getName() + " @ " + f.getEntryPoint() + " =====");
        if (r.decompileCompleted()) {
            out.println(r.getDecompiledFunction().getC());
        } else {
            out.println("// 反编译失败: " + r.getErrorMessage());
        }
        out.println();
        return f;
    }

    @Override
    public void run() throws Exception {
        String outputDir = System.getenv("GHIDRA_OUTPUT_DIR");
        if (outputDir == null || outputDir.isEmpty()) outputDir = ".";
        File outputFile = new File(outputDir, "sendmsg_hunt.c");
        out = new PrintWriter(new FileWriter(outputFile));
        decompiler = new DecompInterface();
        decompiler.setOptions(new DecompileOptions());
        if (!decompiler.openProgram(currentProgram)) { println("decompiler 打开失败"); }
        Memory mem = currentProgram.getMemory();

        String[] needles = {"task_service.cc", "buffer_with_time_post_ui.h", "newsendmsg", "SendMsgFtouser"};
        Set<Long> want = new LinkedHashSet<>();
        for (String s : needles) {
            Address found = mem.findBytes(mem.getMinAddress(), s.getBytes(), null, true, monitor);
            if (found == null) { out.println("// 字符串未见: " + s); continue; }
            out.println("// 字符串 " + s + " @ " + found);
            ReferenceIterator it = currentProgram.getReferenceManager().getReferencesTo(found);
            int n = 0;
            while (it.hasNext()) {
                Reference ref = it.next();
                Function rf = getFunctionContaining(ref.getFromAddress());
                if (rf != null) { want.add(rf.getEntryPoint().getOffset()); n++; }
            }
            out.println("//   xref 函数数: " + n);
        }
        // 已知锚点
        long[] anchors = {0x490fb20L, 0x46391acL, 0x60ab310L};
        for (long v : anchors) want.add(v);

        for (Long v : want) {
            if (monitor.isCancelled()) break;
            decompileAt(v, "hunt");
        }
        out.close();
        println("SendMsgHunt 完成 → " + outputFile.getAbsolutePath());
    }
}
