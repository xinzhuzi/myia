import ghidra.app.script.GhidraScript;
import ghidra.app.decompiler.DecompInterface;
import ghidra.app.decompiler.DecompileResults;
import ghidra.program.model.listing.Function;
import java.io.File;
import java.io.PrintWriter;

public class HuntR24 extends GhidraScript {
    PrintWriter out;
    DecompInterface dec;
    long base;

    @Override
    public void run() throws Exception {
        out = new PrintWriter(new File("/Users/zhengbingjin/ghidra-hunt-r9/hunt_r24_out.txt"), "UTF-8");
        dec = new DecompInterface();
        dec.openProgram(currentProgram);
        base = currentProgram.getImageBase().getOffset();
        long[] offs = {0x4bd0e1cL, 0x26779D4L, 0x39d51d8L, 0x39D62ECL};
        String[] names = {"MMStartTask", "textCallback", "req2bufEnter", "req2bufExit"};
        for (int i = 0; i < offs.length; i++) {
            out.println();
            out.println("======== " + names[i] + " rva=0x" + Long.toHexString(offs[i]) + " ========");
            try {
                Function f = getFunctionContaining(toAddr(base + offs[i]));
                if (f == null) { out.println("  (no function)"); continue; }
                out.println("-- func entry=0x" + Long.toHexString(f.getEntryPoint().getOffset() - base)
                    + " delta=" + (offs[i] - (f.getEntryPoint().getOffset() - base)));
                DecompileResults res = dec.decompileFunction(f, 120, monitor);
                if (res.decompileCompleted()) {
                    String[] lines = res.getDecompiledFunction().getC().split("\n");
                    for (int j = 0; j < lines.length && j < 45; j++) out.println(lines[j]);
                    if (lines.length > 45) out.println("/* truncated */");
                } else out.println("  DECOMP FAILED");
            } catch (Exception e) { out.println("  ERR " + e.getMessage()); }
            out.flush();
        }
        out.println();
        out.println("HUNT_R24_DONE");
        out.close();
        dec.dispose();
    }
}
