import ghidra.app.script.GhidraScript;
import ghidra.app.decompiler.*;
import ghidra.program.model.address.Address;
import ghidra.program.model.listing.Function;
import java.io.File;

public class DecompileTargets extends GhidraScript {
    @Override
    public void run() throws Exception {
        String outDir = "/Users/zhengbingjin/Downloads/rea-wechat-decompile/ghidra_out";
        new File(outDir).mkdirs();
        String[] targets = {"0x31ab38c", "0x5e1d050", "0x48a9a38", "0x88a8fb0"};
        DecompInterface di = new DecompInterface();
        di.setOptions(new DecompileOptions());
        di.openProgram(currentProgram);
        long base = currentProgram.getImageBase().getOffset();
        println("image_base=0x" + Long.toHexString(base));
        for (String t : targets) {
            long off = Long.decode(t);
            Address a = currentProgram.getAddressFactory().getDefaultAddressSpace().getAddress(off);
            Function f = getFunctionAt(a);
            if (f == null) f = getFunctionContaining(a);
            if (f == null) f = createFunction(a, "target_" + t);
            if (f == null) { println("MISS " + t); continue; }
            DecompileResults res = di.decompileFunction(f, 180, monitor);
            String c = (res.getDecompiledFunction() != null)
                ? res.getDecompiledFunction().getC()
                : ("// decompile failed: " + res.getErrorMessage());
            File out = new File(outDir, "func_" + t + "_" + Long.toHexString(f.getEntryPoint().getOffset()) + ".c");
            java.nio.file.Files.write(out.toPath(), c.getBytes());
            println("WROTE " + t + " -> " + out.getName() + " size=" + c.length());
        }
        di.dispose();
        println("DECOMPILE_TARGETS_DONE");
    }
}
