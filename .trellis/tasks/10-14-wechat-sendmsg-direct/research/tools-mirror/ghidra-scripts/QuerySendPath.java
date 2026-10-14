import ghidra.app.script.GhidraScript;
import ghidra.program.model.address.Address;
import ghidra.program.model.listing.Function;
import ghidra.program.model.listing.FunctionIterator;
import ghidra.program.model.symbol.Reference;
import ghidra.program.model.symbol.ReferenceIterator;
import java.io.File;
import java.io.PrintWriter;

public class QuerySendPath extends GhidraScript {
    PrintWriter out;
    String af(long v) { return currentProgram.getAddressFactory().getDefaultAddressSpace().getAddress(v).toString(); }

    void dumpRefsTo(long target, String label) {
        out.println("== refs to " + af(target) + " (" + label + ") ==");
        try {
            Address a = toAddr(target);
            ReferenceIterator it = currentProgram.getReferenceManager().getReferencesTo(a);
            int n = 0;
            while (it.hasNext()) {
                Reference r = it.next();
                if (r.getReferenceType().isCall() || r.getReferenceType().isData()) {
                    Function f = getFunctionContaining(r.getFromAddress());
                    String fname = f != null ? (f.getName() + "@" + f.getEntryPoint()) : "?";
                    out.println("  " + r.getFromAddress() + " type=" + r.getReferenceType() + " in " + fname);
                    if (++n > 60) { out.println("  ...(truncated)"); break; }
                }
            }
            if (n == 0) out.println("  (none)");
        } catch (Exception e) { out.println("  ERR " + e.getMessage()); }
    }

    @Override
    public void run() throws Exception {
        File f = new File("/Users/zhengbingjin/Downloads/rea-wechat-decompile/sendpath_query.txt");
        out = new PrintWriter(f, "UTF-8");

        out.println("== functions whose name contains send/Msg (case-insens) ==");
        FunctionIterator fi = currentProgram.getFunctionManager().getFunctions(true);
        int n = 0;
        while (fi.hasNext()) {
            Function fun = fi.next();
            String nm = fun.getName();
            String low = nm.toLowerCase();
            if ((low.contains("sendmsg") || low.contains("sendmessage") || low.contains("sendtext")
                || low.contains("sendim") || low.contains("ftouser")) && !low.contains("wetyped")) {
                out.println("  " + fun.getEntryPoint() + "  " + nm);
                if (++n > 200) { out.println("  ...(truncated)"); break; }
            }
        }
        out.println("  total=" + n);

        dumpRefsTo(0x490fb20L, "task-submitter");
        dumpRefsTo(0x46391acL, "completion-callback");
        dumpRefsTo(0x5e1d050L, "rpc-stub");

        out.println("== refs to task_service.cc string ==");
        try {
            Address found = find(toAddr(0), "task_service.cc".getBytes("UTF-8"));
            int k = 0;
            while (found != null && k < 5) {
                out.println("  string at " + found);
                ReferenceIterator it = currentProgram.getReferenceManager().getReferencesTo(found);
                int m = 0;
                while (it.hasNext()) {
                    Reference r = it.next();
                    Function f = getFunctionContaining(r.getFromAddress());
                    out.println("    ref from " + r.getFromAddress() + " in " + (f != null ? f.getName() + "@" + f.getEntryPoint() : "?"));
                    if (++m > 20) break;
                }
                found = find(found.add(1), "task_service.cc".getBytes("UTF-8"));
                k++;
            }
        } catch (Exception e) { out.println("  ERR " + e.getMessage()); }

        out.close();
        println("QUERY_DONE");
    }
}
