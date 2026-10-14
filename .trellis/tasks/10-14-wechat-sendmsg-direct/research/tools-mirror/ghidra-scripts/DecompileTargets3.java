import ghidra.app.script.GhidraScript;
import ghidra.app.decompiler.*;
import ghidra.program.model.address.Address;
import ghidra.program.model.listing.Function;
import java.io.File;

public class DecompileTargets3 extends GhidraScript {
    @Override
    public void run() throws Exception {
        String outDir = "/Users/zhengbingjin/Downloads/微信反编译/sendmsg-勘察-1014/decomp";
        new File(outDir).mkdirs();
        long[] targets = {0x490b0ecL, 0x490f0f8L, 0x5a2beb0L, 0x5a2d5e8L, 0x5bc97e8L, 0x5d38500L, 0x5d75d14L};
        DecompInterface di = new DecompInterface();
        di.setOptions(new DecompileOptions());
        di.openProgram(currentProgram);
        for (long t : targets) {
            Address a = toAddr(t);
            Function f = getFunctionContaining(a);
            if (f == null) f = createFunction(a, "site_" + Long.toHexString(t));
            if (f == null) { println("MISS " + Long.toHexString(t)); continue; }
            DecompileResults res = di.decompileFunction(f, 240, monitor);
            String c = (res.getDecompiledFunction() != null)
                ? res.getDecompiledFunction().getC()
                : ("// decompile failed: " + res.getErrorMessage());
            File out = new File(outDir, "site_" + Long.toHexString(t) + "_fn_" + Long.toHexString(f.getEntryPoint().getOffset()) + ".c");
            java.nio.file.Files.write(out.toPath(), c.getBytes());
            println("WROTE site=" + Long.toHexString(t) + " fn=" + Long.toHexString(f.getEntryPoint().getOffset()) + " size=" + c.length());
        }
        di.dispose();
        println("DT3_DONE");
    }
}
