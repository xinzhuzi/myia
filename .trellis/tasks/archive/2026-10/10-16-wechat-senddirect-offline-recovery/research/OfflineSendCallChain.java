// Read-only extraction from an existing Ghidra project; no target execution.
import ghidra.app.script.GhidraScript;
import ghidra.app.decompiler.DecompInterface;
import ghidra.app.decompiler.DecompileResults;
import ghidra.program.model.address.Address;
import ghidra.program.model.listing.Function;
import ghidra.program.model.listing.Instruction;
import ghidra.program.model.listing.InstructionIterator;
import ghidra.program.model.symbol.Reference;
import java.io.PrintWriter;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.StandardOpenOption;

public class OfflineSendCallChain extends GhidraScript {
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
        try (PrintWriter meta = newFile(output.resolve("offline-program.tsv"))) {
            meta.println("name\t" + currentProgram.getName());
            meta.println("executable_sha256\t" + sha256);
            meta.println("executable_path\t" + currentProgram.getExecutablePath());
            meta.println("language\t" + currentProgram.getLanguageID());
            meta.println("image_base\t0x" + Long.toHexString(base));
        }
        long[] targets = {0x5980a6cL, 0x5980d74L, 0x5971c24L, 0x597d26cL,
                          0x5ded378L, 0x56300b4L, 0x5ab3f98L};
        DecompInterface decompiler = new DecompInterface();
        if (!decompiler.openProgram(currentProgram)) throw new IllegalStateException(decompiler.getLastMessage());
        try (PrintWriter index = newFile(output.resolve("offline-functions.tsv"))) {
            for (long rva : targets) {
                monitor.checkCancelled();
                Address address = toAddr(base + rva);
                Function function = getFunctionAt(address);
                if (function == null) function = getFunctionContaining(address);
                String stem = "offline-fn-" + Long.toHexString(rva);
                if (function == null) {
                    index.println("0x" + Long.toHexString(rva) + "\tMISSING_FUNCTION");
                    index.flush();
                    continue;
                }
                DecompileResults result = decompiler.decompileFunction(function, 25, monitor);
                index.println("0x" + Long.toHexString(rva) + "\t" + function.getEntryPoint()
                    + "\t" + function.getName() + "\t" + result.decompileCompleted()
                    + "\t" + function.getBody().getNumAddresses());
                index.flush();
                try (PrintWriter code = newFile(output.resolve(stem + ".c"))) {
                    code.println("// Ghidra inferred pseudocode; requested=0x" + Long.toHexString(rva));
                    code.println("// entry=" + function.getEntryPoint() + " end=" + function.getBody().getMaxAddress());
                    code.println(result.decompileCompleted() ? result.getDecompiledFunction().getC() : result.getErrorMessage());
                }
                try (PrintWriter asm = newFile(output.resolve(stem + ".asm"))) {
                    InstructionIterator instructions = currentProgram.getListing().getInstructions(function.getBody(), true);
                    while (instructions.hasNext()) {
                        Instruction instruction = instructions.next();
                        StringBuilder bytes = new StringBuilder();
                        for (byte value : instruction.getBytes()) bytes.append(String.format("%02x", value & 255));
                        asm.println("0x" + Long.toHexString(instruction.getAddress().getOffset() - base)
                            + "\t" + bytes + "\t" + instruction);
                    }
                }
                try (PrintWriter refs = newFile(output.resolve(stem + ".refs.tsv"))) {
                    Reference[] references = getReferencesTo(function.getEntryPoint());
                    refs.println("total\t" + references.length + "\toutput_limit\t64");
                    for (int i = 0; i < Math.min(64, references.length); i++) {
                        Reference ref = references[i];
                        Function caller = getFunctionContaining(ref.getFromAddress());
                        refs.println(ref.getFromAddress() + "\t" + ref.getReferenceType() + "\t"
                            + (caller == null ? "NO_FUNCTION" : caller.getEntryPoint() + " " + caller.getName()));
                    }
                }
                println("Extracted " + stem + " completed=" + result.decompileCompleted());
            }
        } finally {
            decompiler.dispose();
        }
    }
}
