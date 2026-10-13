import ghidra.app.script.GhidraScript;
import ghidra.app.decompiler.DecompInterface;
import ghidra.app.decompiler.DecompileResults;
import ghidra.program.model.address.Address;
import ghidra.program.model.listing.Data;
import ghidra.program.model.listing.DataIterator;
import ghidra.program.model.listing.Function;
import ghidra.program.model.listing.Listing;
import ghidra.program.model.mem.Memory;
import ghidra.program.model.mem.MemoryBlock;
import ghidra.program.model.symbol.Reference;
import ghidra.program.model.symbol.ReferenceIterator;
import java.io.FileWriter;
import java.io.PrintWriter;
import java.nio.charset.StandardCharsets;
import java.util.*;

//@category Analysis
public class HuntXref extends GhidraScript {

    private PrintWriter out;
    private DecompInterface di;

    private void P(String s) {
        println(s);
        if (out != null) out.println(s);
    }

    private void dumpXrefs(String tag, Address target) {
        P("---- XREFS TO " + target + " (" + tag + ") ----");
        ReferenceIterator it = currentProgram.getReferenceManager().getReferencesTo(target);
        int n = 0;
        while (it.hasNext()) {
            Reference r = it.next();
            n++;
            Address from = r.getFromAddress();
            Function f = getFunctionContaining(from);
            String fs = (f == null) ? "-" : (f.getName() + "@" + f.getEntryPoint());
            P("  xref from " + from + " type=" + r.getReferenceType() + " in " + fs);
            // two-hop: if 'from' is itself data (selref/pointer), show refs to it
            ReferenceIterator it2 = currentProgram.getReferenceManager().getReferencesTo(from);
            while (it2.hasNext()) {
                Reference r2 = it2.next();
                Address f2 = r2.getFromAddress();
                Function g = getFunctionContaining(f2);
                String gs = (g == null) ? "-" : (g.getName() + "@" + g.getEntryPoint());
                P("    hop2 from " + f2 + " type=" + r2.getReferenceType() + " in " + gs);
            }
        }
        P("  total direct xrefs: " + n);
    }

    private void dumpQwords(Address start, int count) {
        P("---- QWORDS at " + start + " x" + count + " ----");
        Memory m = currentProgram.getMemory();
        for (int i = 0; i < count; i++) {
            Address a = start.add(i * 8L);
            try {
                long v = m.getLong(a);
                String extra = "";
                Data d = currentProgram.getListing().getDataAt(a);
                if (d != null && d.hasStringValue()) extra = " \"" + d.getValue() + "\"";
                P("  [" + a + "] = 0x" + Long.toHexString(v) + extra);
            } catch (Exception e) {
                P("  [" + a + "] = <unreadable>");
            }
        }
    }

    // scan ALL initialized blocks for 8-byte little-endian value
    private List<Address> findPtr(long value, int limit) {
        List<Address> hits = new ArrayList<>();
        Memory m = currentProgram.getMemory();
        for (MemoryBlock b : m.getBlocks()) {
            if (!b.isInitialized()) continue;
            Address a = b.getStart();
            Address end = b.getEnd();
            while (a.compareTo(end) < 0 && hits.size() < limit) {
                try {
                    if (m.getLong(a) == value) hits.add(a);
                } catch (Exception e) { /* skip */
                }
                a = a.add(8);
            }
        }
        return hits;
    }

    // find relative-method-list header owning entry at 'entry', then find owner class_ro
    private void mlistOwner(Address entry) throws Exception {
        Memory m = currentProgram.getMemory();
        P("#### MLIST owner hunt for entry @ " + entry);
        Address found = null;
        for (int back = 4; back <= 8192; back += 4) {
            Address h = entry.add(-back);
            try {
                long q = m.getLong(h);
                int v = (int) (q & 0xffffffffL);
                if (v != 0x8000000c) continue;
                int cnt = (int) ((q >> 32) & 0xffffffffL);
                long span = 8L + 12L * cnt;
                long off = entry.getOffset() - h.getOffset() - 8;
                if (off >= 0 && off % 12 == 0 && off < span) {
                    found = h;
                    P("  method list header @ " + h + " entsize=0x" + Integer.toHexString(v) + " count=" + cnt);
                    break;
                }
            } catch (Exception e) { continue; }
        }
        if (found == null) { P("  no header found"); return; }
        for (Address site : findPtr(found.getOffset(), 16)) {
            P("  ptr-to-list @ " + site + " (likely class_ro_t.baseMethods / class_rw_t.methods)");
            dumpQwords(site.add(-0x20), 10);
        }
    }

    private void dumpDecomp(String tag, Address addr) {
        Function f = (addr != null) ? getFunctionContaining(addr) : null;
        if (f == null) { P("---- DECOMP " + tag + " " + addr + ": no containing function ----"); return; }
        P("==== DECOMP " + tag + " func " + f.getName() + " @ " + f.getEntryPoint() + " size=" + f.getBody().getNumAddresses() + " ====");
        DecompileResults res = di.decompileFunction(f, 240, monitor);
        if ((res == null || !res.decompileCompleted()) && !monitor.isCancelled()) {
            P("  retrying decompile...");
            res = di.decompileFunction(f, 240, monitor);
        }
        if (res != null && res.decompileCompleted()) {
            String c = res.getDecompiledFunction().getC();
            for (String line : c.split("\n")) P("| " + line);
        } else {
            P("  decompile failed: " + (res == null ? "null" : res.getErrorMessage()));
        }
        // callers summary
        P("  -- callers of " + f.getName() + " --");
        ReferenceIterator it = currentProgram.getReferenceManager().getReferencesTo(f.getEntryPoint());
        int shown = 0;
        while (it.hasNext() && shown < 40) {
            Reference r = it.next();
            if (r.getReferenceType().isCall()) {
                P("    called from " + r.getFromAddress());
                shown++;
            }
        }
    }

    @Override
    public void run() throws Exception {
        String[] args = getScriptArgs();
        String outFile = null;
        List<String> todo = new ArrayList<>();
        for (String a : args) {
            if (a.startsWith("out=")) outFile = a.substring(4);
            else todo.add(a);
        }
        if (outFile != null) out = new PrintWriter(new FileWriter(outFile));
        di = new DecompInterface();
        boolean opened = di.openProgram(currentProgram);
        P("### DecompInterface.openProgram = " + opened);

        P("### HuntXref on " + currentProgram.getName() + " imageBase=" + currentProgram.getImageBase());

        for (String a : todo) {
            try {
                if (a.startsWith("xref:")) {
                    Address t = currentProgram.getAddressFactory().getAddress(a.substring(5));
                    dumpXrefs(a, t);
                } else if (a.startsWith("qwords:")) {
                    String[] p = a.substring(7).split(":");
                    dumpQwords(currentProgram.getAddressFactory().getAddress(p[0]), Integer.parseInt(p[1]));
                } else if (a.startsWith("findptr:")) {
                    long v = Long.parseLong(a.substring(8).replace("0x", ""), 16);
                    P("---- FINDPTR 0x" + Long.toHexString(v) + " ----");
                    for (Address h : findPtr(v, 64)) {
                        Data d = currentProgram.getListing().getDataAt(h);
                        P("  ptr @ " + h + (d != null ? " (" + d.getDataType().getDisplayName() + ")" : ""));
                    }
                } else if (a.startsWith("typeinfo:")) {
                    Address nameAddr = currentProgram.getAddressFactory().getAddress(a.substring(9));
                    P("#### TYPEINFO chain for name string @ " + nameAddr);
                    // step1: find typeinfo objects referencing the name (xref + raw scan)
                    Set<Address> tiObjects = new LinkedHashSet<>();
                    ReferenceIterator it = currentProgram.getReferenceManager().getReferencesTo(nameAddr);
                    while (it.hasNext()) {
                        Reference r = it.next();
                        Address from = r.getFromAddress();
                        P("  name xref from " + from + " type=" + r.getReferenceType());
                        tiObjects.add(from.add(-8)); // name field is at +8 in typeinfo
                    }
                    if (tiObjects.isEmpty()) {
                        for (Address h : findPtr(nameAddr.getOffset(), 64)) tiObjects.add(h.add(-8));
                    }
                    for (Address ti : tiObjects) {
                        P("  candidate typeinfo object @ " + ti);
                        dumpQwords(ti, 4);
                        // step2: vtables point to typeinfo at slot+8
                        List<Address> vslots = findPtr(ti.getOffset(), 16);
                        for (Address vs : vslots) {
                            Address vtable = vs.add(-8);
                            P("  => vtable @ " + vtable + " (typeinfo slot @ " + vs + ")");
                            dumpQwords(vtable, 14);
                            P("  -- refs to vtable --");
                            ReferenceIterator it3 = currentProgram.getReferenceManager().getReferencesTo(vtable);
                            while (it3.hasNext()) {
                                Reference r3 = it3.next();
                                Address f3 = r3.getFromAddress();
                                Function g = getFunctionContaining(f3);
                                P("    from " + f3 + " type=" + r3.getReferenceType() + " in " +
                                        (g == null ? "-" : g.getName() + "@" + g.getEntryPoint()));
                            }
                        }
                    }
                } else if (a.startsWith("decomp:")) {
                    Address t = currentProgram.getAddressFactory().getAddress(a.substring(7));
                    dumpDecomp(a, t);
                } else if (a.startsWith("mlist:")) {
                    mlistOwner(currentProgram.getAddressFactory().getAddress(a.substring(6)));
                } else if (a.startsWith("strfind:")) {
                    String needle = a.substring(8);
                    byte[] pat = (needle + "\0").getBytes(StandardCharsets.US_ASCII);
                    Memory m = currentProgram.getMemory();
                    Address cur = m.getMinAddress();
                    int hits = 0;
                    P("---- STRFIND \"" + needle + "\" ----");
                    while (hits < 40) {
                        Address f = m.findBytes(cur, m.getMaxAddress(), pat, null, true, monitor);
                        if (f == null) break;
                        int xn = 0;
                        ReferenceIterator it = currentProgram.getReferenceManager().getReferencesTo(f);
                        while (it.hasNext()) { it.next(); xn++; }
                        P("  @ " + f + " xrefs=" + xn);
                        hits++;
                        cur = f.add(1);
                    }
                } else {
                    P("!! unknown arg: " + a);
                }
            } catch (Exception e) {
                P("!! arg " + a + " failed: " + e);
            }
        }
        if (out != null) { out.flush(); out.close(); }
    }
}
