// Read-only extraction from an existing Ghidra project; no target execution.
// 10-19 终验修正位导出:0x5a6c374(栈对象构建/门字节写入者) 0x5a6c868 0x5a6c8a0(崩点消费链)
import ghidra.app.script.GhidraScript;
import ghidra.app.decompiler.DecompInterface;
import ghidra.app.decompiler.DecompileResults;
import ghidra.program.model.address.Address;
import ghidra.program.model.listing.Function;
import ghidra.program.model.listing.Instruction;
import ghidra.program.model.listing.InstructionIterator;
import java.io.PrintWriter;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.StandardOpenOption;

public class DumpFixTargets extends GhidraScript {
    private PrintWriter newFile(Path path) throws Exception {
        return new PrintWriter(Files.newBufferedWriter(path, StandardOpenOption.CREATE_NEW));
    }
    @Override
    public void run() throws Exception {
        String[] args = getScriptArgs();
        if (args.length != 2) throw new IllegalArgumentException("output-dir expected-sha256");
        Path output = Path.of(args[0]);
        String sha256 = currentProgram.getExecutableSHA256();
        if (!args[1].equals(sha256)) throw new IllegalStateException("Database input hash mismatch: " + sha256);
        long base = currentProgram.getImageBase().getOffset();
        long[] targets = {0x5a6c22cL};
        DecompInterface decompiler = new DecompInterface();
        if (!decompiler.openProgram(currentProgram)) throw new IllegalStateException(decompiler.getLastMessage());
        try (PrintWriter index = newFile(output.resolve("fix-functions.tsv"))) {
            for (long rva : targets) {
                monitor.checkCancelled();
                Address address = toAddr(base + rva);
                Function function = getFunctionAt(address);
                if (function == null) function = getFunctionContaining(address);
                String stem = "fix-fn-" + Long.toHexString(rva);
                if (function == null) {
                    index.println("0x" + Long.toHexString(rva) + "\tMISSING_FUNCTION");
                    index.flush();
                    continue;
                }
                DecompileResults result = decompiler.decompileFunction(function, 30, monitor);
                index.println("0x" + Long.toHexString(rva) + "\t" + function.getEntryPoint()
                    + "\t" + function.getName() + "\t" + result.decompileCompleted()
                    + "\t" + function.getBody().getNumAddresses());
                index.flush();
                try (PrintWriter code = newFile(output.resolve(stem + ".c"))) {
                    code.println("// requested=0x" + Long.toHexString(rva));
                    code.println("// entry=" + function.getEntryPoint() + " end=" + function.getBody().getMaxAddress());
                    code.println(result.decompileCompleted() ? result.getDecompiledFunction().getC() : result.getErrorMessage());
                }
                try (PrintWriter asm = newFile(output.resolve(stem + ".asm"))) {
                    asm.println("// " + function.getName() + " " + function.getEntryPoint());
                    InstructionIterator it = currentProgram.getListing().getInstructions(function.getBody(), true);
                    while (it.hasNext()) {
                        Instruction ins = it.next();
                        asm.println(ins.getAddress() + "\t" + ins.toString());
                    }
                }
            }
        }
        decompiler.dispose();
    }
}
