"""Synthetic object graphs exercise the bounded service snapshot without LLDB."""
from __future__ import annotations

import unittest

from newsendmsg_identity_4115 import inspect_service


class IdentitySnapshotChecks(unittest.TestCase):
    def graph(self, base):
        account, control = 0x500000000, 0x600000000
        owner, service = control + 0x18, control + 0x28
        return {base + 0xA45DF38: account, account: base + 0x9E92400,
                base + 0x9E92418: base + 0x466A318,
                account + 0x250: service, account + 0x258: control,
                control: base + 0x9E92C98, control + 0x18: base + 0x9E8FC30,
                control + 0x28: base + 0x9E8FDA0,
                owner + 8: base + 0x9E8FD78,
                base + 0x9E8FDC8: base + 0x46353A0}

    def test_actual_alias_layout(self):
        # shared_ptr control embeds owner; control+0x18 is owner's vptr,
        # not a pointer to owner. The inspection must honor that distinction.
        for base in (0x100000000, 0x200004000):
            graph = self.graph(base)
            reads = []

            def read(address, size):
                self.assertEqual(size, 8)
                reads.append(address)
                return graph[address].to_bytes(8, 'little')

            result = inspect_service(read, base)
            self.assertTrue(result['identity_matched'])
            self.assertEqual(result['reads'], len(reads))
            self.assertEqual(result['bytes_read'], 80)
            self.assertEqual(result['service_interface'], hex(0x600000028))
            self.assertFalse(result['native_called'])
            self.assertFalse(result['sent'])

    def test_each_identity_corruption_is_rejected(self):
        base = 0x100000000
        for address in self.graph(base):
            graph = self.graph(base)
            graph[address] = 0
            with self.subTest(address=hex(address)), self.assertRaises(RuntimeError):
                inspect_service(lambda address, size: graph[address].to_bytes(8, 'little'), base)

    def test_wrong_alias_relationship_is_rejected(self):
        base = 0x100000000
        graph = self.graph(base)
        graph[0x500000258] += 8
        with self.assertRaisesRegex(RuntimeError, 'relationship'):
            inspect_service(lambda address, size: graph[address].to_bytes(8, 'little'), base)

    def test_short_reads_and_cancellation_propagate(self):
        for raw in (b'', bytes(7), bytearray(8)):
            with self.subTest(raw=raw), self.assertRaises(RuntimeError):
                inspect_service(lambda address, size: raw, 0x100000000)

        def cancelled(address, size):
            raise InterruptedError('cancelled')

        with self.assertRaises(InterruptedError):
            inspect_service(cancelled, 0x100000000)

    def test_invalid_base_never_reads(self):
        def forbidden(address, size):
            self.fail('invalid base must not read')

        for base in (0, 1, True, 0x100000001, '1'):
            with self.subTest(base=base), self.assertRaises(ValueError):
                inspect_service(forbidden, base)


if __name__ == '__main__':
    unittest.main(verbosity=2)
