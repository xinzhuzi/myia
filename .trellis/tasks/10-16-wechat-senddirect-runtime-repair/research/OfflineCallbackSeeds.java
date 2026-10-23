// Bounded references from the existing verified database, never target execution.
import ghidra.app.script.GhidraScript;
import ghidra.program.model.address.Address;
import ghidra.program.model.listing.Data;
import ghidra.program.model.listing.Function;
import ghidra.program.model.symbol.Reference;
import java.io.PrintWriter;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.StandardOpenOption;

public class OfflineCallbackSeeds extends GhidraScript {
    @Override
    public void run() throws Exception {
        String[] args = getScriptArgs();
        if (args.length < 3 || args.length > 10) throw new IllegalArgumentException("out sha seed...");
        if (!args[1].equals(currentProgram.getExecutableSHA256())) throw new IllegalStateException("wrong binary");
        Path output = Path.of(args[0]);
        try (PrintWriter rows = new PrintWriter(Files.newBufferedWriter(output.resolve("callback-seeds.tsv"),
                                                   StandardOpenOption.CREATE_NEW))) {
            for (int index = 2; index < args.length; index++) {
                monitor.checkCancelled();
                Address seed = toAddr(Long.decode(args[index]));
                Data data = getDataAt(seed);
                rows.println("SEED\t" + seed + "\t" + (data == null ? "NO_DATA" : data.getDefaultValueRepresentation()));
                Address[] targets = data != null && data.getValue() instanceof Address
                    ? new Address[]{seed, (Address)data.getValue()} : new Address[]{seed};
                for (Address target : targets) {
                    Reference[] refs = getReferencesTo(target);
                    rows.println("REFS\t" + target + "\t" + refs.length);
                    for (int i = 0; i < Math.min(64, refs.length); i++) {
                        Reference ref = refs[i];
                        Function function = getFunctionContaining(ref.getFromAddress());
                        Data source = getDataAt(ref.getFromAddress());
                        rows.println(target + "\t" + ref.getFromAddress() + "\t" + ref.getReferenceType()
                            + "\t" + (function == null ? "NO_FUNCTION" : function.getEntryPoint() + " " + function.getName())
                            + "\t" + (source == null ? "" : source.getDefaultValueRepresentation()));
                    }
                }
            }
        }
        println("Callback seed references retained; no analysis or target execution");
    }
}
