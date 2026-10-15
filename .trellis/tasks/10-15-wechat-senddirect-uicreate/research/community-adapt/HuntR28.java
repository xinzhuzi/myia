import ghidra.app.script.GhidraScript;
import ghidra.app.decompiler.DecompInterface;
import ghidra.app.decompiler.DecompileResults;
import ghidra.program.model.listing.Function;
import java.io.File;
import java.io.PrintWriter;

public class HuntR28 extends GhidraScript {
    PrintWriter out;
    DecompInterface dec;
    long base;

    @Override
    public void run() throws Exception {
        out = new PrintWriter(new File("/Users/zhengbingjin/ghidra-hunt-r9/hunt_r28_out.txt"), "UTF-8");
        dec = new DecompInterface();
        dec.openProgram(currentProgram);
        base = currentProgram.getImageBase().getOffset();
        long[] offs = {0x5dd16d8L, 0x5980decL};
        String[] names = {"AUTOBUF_DELTA_CAND", "BUF2RESP_CAND"};
        for (int i = 0; i < offs.length; i++) {
            out.println();
            out.println("======== " + names[i] + " rva=0x" + Long.toHexString(offs[i]) + " ========");
            Function f = getFunctionContaining(toAddr(base + offs[i]));
            if (f == null) { out.println("  (no function)"); continue; }
            out.println("-- entry=0x" + Long.toHexString(f.getEntryPoint().getOffset() - base));
            DecompileResults res = dec.decompileFunction(f, 120, monitor);
            if (res.decompileCompleted()) {
                String[] lines = res.getDecompiledFunction().getC().split("\n");
                for (int j = 0; j < lines.length && j < 40; j++) out.println(lines[j]);
            } else out.println("  FAILED");
            out.flush();
        }
        out.println("HUNT_R28_DONE");
        out.close();
        dec.dispose();
    }
}
