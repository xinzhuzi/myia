import ghidra.app.script.GhidraScript;
import ghidra.app.decompiler.*;
import ghidra.program.model.address.Address;
import ghidra.program.model.listing.Function;
import java.io.File;

public class DecompileTargets4 extends GhidraScript {
    @Override
    public void run() throws Exception {
        String outDir = "/Users/zhengbingjin/Downloads/微信反编译/sendmsg-勘察-1014/decomp";
        long[] targets = {0x5a2b978L, 0x5a2b788L};
        DecompInterface di = new DecompInterface();
        di.setOptions(new DecompileOptions());
        di.openProgram(currentProgram);
        for (long t : targets) {
            Address a = toAddr(t);
            Function f = getFunctionAt(a);
            if (f == null) f = createFunction(a, "marshal_" + Long.toHexString(t));
            if (f == null) { println("MISS " + Long.toHexString(t)); continue; }
            DecompileResults res = di.decompileFunction(f, 300, monitor);
            String c = (res.getDecompiledFunction() != null)
                ? res.getDecompiledFunction().getC()
                : ("// decompile failed: " + res.getErrorMessage());
            File out = new File(outDir, "marshal_" + Long.toHexString(t) + ".c");
            java.nio.file.Files.write(out.toPath(), c.getBytes());
            println("WROTE " + Long.toHexString(t) + " size=" + c.length());
        }
        di.dispose();
        println("DT4_DONE");
    }
}
