"""N1 tools: measure whether Android apps use post-quantum TLS.

  python n1_tools.py pcap capture.pcap [more.pcap ...]   -> CSV: one row per TLS connection (TCP)
  python n1_tools.py apk  app.apk [more.apk ...]         -> which networking framework each APK uses
  python n1_tools.py timing host [n]                     -> TLS handshake time: post-quantum vs classic (ms)
  python n1_tools.py shortcuts host [host ...]           -> key-share reuse + RSA key transport (sessions per Shor run)
  python n1_tools.py analyze connections.csv [servers.csv] -> per-app 2x2 outcome, headline % with 95% CI,
                                                            McNemar old-vs-new phone (needs columns below)
  python n1_tools.py selftest                            -> checks the pcap, apk and analyze tools (offline)

analyze expects connections.csv columns: app, device, first_party (yes/no), sni, client_offers_pq_keyshare,
pq_negotiated (as written by the pcap command + your log columns). servers.csv = f2_starter.py output.

pcap: classic .pcap (PCAPdroid export, or Wireshark "Save As -> pcap"). Reads only the plaintext
ClientHello/ServerHello, nothing is decrypted. QUIC/HTTP3 flows are not parsed here: look at them in the
Wireshark GUI (filter: quic && tls.handshake.type == 1), which decrypts QUIC Initial packets itself.
"""
import re, struct, sys, zipfile

GROUPS = {0x0017: "secp256r1", 0x0018: "secp384r1", 0x0019: "secp521r1", 0x001D: "X25519", 0x001E: "X448",
          0x11EB: "SecP256r1MLKEM768", 0x11EC: "X25519MLKEM768", 0x11ED: "SecP384r1MLKEM1024",
          0x0200: "MLKEM512", 0x0201: "MLKEM768", 0x0202: "MLKEM1024", 0x6399: "X25519Kyber768Draft00"}
PQ = {0x11EB, 0x11EC, 0x11ED, 0x0200, 0x0201, 0x0202, 0x6399}
SUITES = {0x1301: "AES_128_GCM", 0x1302: "AES_256_GCM", 0x1303: "CHACHA20_POLY1305"}   # TLS 1.3 (Grover view)
HRR_RANDOM = bytes.fromhex("CF21AD74E59A6111BE1D8C021E65B891C2A211167ABB8C5E079E09E2C8A8339C")

def name(g): return GROUPS.get(g, hex(g))
def u16(b, i): return int.from_bytes(b[i:i + 2], "big")

# ---------------- pcap -> TCP streams ----------------
def read_pcap(path):
    data = open(path, "rb").read()
    if data[:4] in (b"\xd4\xc3\xb2\xa1", b"\x4d\x3c\xb2\xa1"): end = "<"
    elif data[:4] in (b"\xa1\xb2\xc3\xd4", b"\xa1\xb2\x3c\x4d"): end = ">"
    else: sys.exit(f"{path}: not a classic pcap (pcapng? In Wireshark use File > Save As > pcap)")
    link = struct.unpack(end + "I", data[20:24])[0]
    i = 24
    while i + 16 <= len(data):
        n = struct.unpack(end + "I", data[i + 8:i + 12])[0]
        yield link, data[i + 16:i + 16 + n]
        i += 16 + n

def ip_payload(link, frame):
    if link == 1:   # Ethernet (Wireshark on a laptop hotspot)
        etype, frame = u16(frame, 12), frame[14:]
        if etype == 0x8100: etype, frame = u16(frame, 2), frame[4:]   # VLAN tag
    elif link == 113: frame = frame[16:]                              # Linux cooked (tcpdump -i any)
    elif link not in (101, 228, 229): return None                     # raw IP (PCAPdroid)
    if frame[:1] and frame[0] >> 4 == 4 and frame[9] == 6:
        h = (frame[0] & 15) * 4
        return frame[12:16], frame[16:20], frame[h:]
    if frame[:1] and frame[0] >> 4 == 6 and frame[6] == 6:
        return frame[8:24], frame[24:40], frame[40:]
    return None

def tcp_streams(paths):
    segs, isn = {}, {}
    for path in paths:
        for link, frame in read_pcap(path):
            p = ip_payload(link, frame)
            if not p: continue
            src, dst, tcp = p
            sport, dport, seq = u16(tcp, 0), u16(tcp, 2), int.from_bytes(tcp[4:8], "big")
            key = (src, sport, dst, dport)
            if tcp[13] & 0x02: isn[key] = seq + 1                     # SYN
            payload = tcp[(tcp[12] >> 4) * 4:]
            if payload: segs.setdefault(key, {}).setdefault(seq, payload)
    streams = {}
    for key, s in segs.items():
        pos, out = isn.get(key, min(s)), b""
        for seq in sorted(s):                                          # reassemble in order, stop at a gap
            if seq > pos: break
            out += s[seq][pos - seq:]
            pos = max(pos, seq + len(s[seq]))
        streams[key] = out
    return streams

# ---------------- TLS hello parsing ----------------
def first_handshake(buf):
    body, i = b"", 0
    while i + 5 <= len(buf) and buf[i] == 22:                          # 22 = handshake record
        n = u16(buf, i + 3)
        body += buf[i + 5:i + 5 + n]
        i += 5 + n
        if len(body) >= 4 and len(body) >= 4 + int.from_bytes(body[1:4], "big"):
            return body[0], body[4:4 + int.from_bytes(body[1:4], "big")]
    return None, None

def hello_extensions(kind, b):
    p = 34 + 1 + b[34]                                                 # version, random, session id
    if kind == 1: p += 2 + u16(b, p); p += 1 + b[p]                     # ClientHello: suites, compression
    else: p += 3                                                        # ServerHello: suite, compression
    exts, end = {}, p + 2 + u16(b, p)
    p += 2
    while p + 4 <= end:
        exts[u16(b, p)] = b[p + 4:p + 4 + u16(b, p + 2)]
        p += 4 + u16(b, p + 2)
    return b[2:34], exts

def client_info(b):
    _, ext = hello_extensions(1, b)
    sni = ext[0][5:5 + u16(ext[0], 3)].decode(errors="replace") if 0 in ext else ""
    supported = [u16(ext[10], i) for i in range(2, 2 + u16(ext.get(10, b"\0\0"), 0), 2)]
    shares, ks, i = [], ext.get(51, b"\0\0"), 2
    while i + 4 <= 2 + u16(ks, 0):
        shares.append(u16(ks, i)); i += 4 + u16(ks, i + 2)
    modes = ext.get(45, b"\0")                                          # psk_key_exchange_modes
    psk_modes = " ".join({0: "psk_ke", 1: "psk_dhe_ke"}.get(m, str(m)) for m in modes[1:1 + modes[0]])
    return sni, supported, shares, 41 in ext, psk_modes                # 41 = pre_shared_key (resumption)

def server_info(b):
    random, ext = hello_extensions(2, b)
    suite = u16(b, 35 + b[34])
    version = "TLS1.3" if u16(ext.get(43, b"\0\0"), 0) == 0x0304 else "TLS1.2-or-older"
    return {"group": u16(ext[51], 0) if 51 in ext else None, "hrr": random == HRR_RANDOM,
            "suite": SUITES.get(suite, hex(suite)), "version": version, "psk_accepted": 41 in ext}

def pcap_report(paths):
    import os
    rows = []
    for path in paths:                                                   # one file at a time: flows never mix
        rows += [dict(capture_file=os.path.basename(path), **r) for r in _pcap_rows(tcp_streams([path]))]
    return rows

def _pcap_rows(streams):
    rows = []
    for (src, sport, dst, dport), data in streams.items():
        kind, body = first_handshake(data)
        if kind != 1: continue
        sni, supported, shares, psk_offered, psk_modes = client_info(body)
        skind, sbody = first_handshake(streams.get((dst, dport, src, sport), b""))
        s = server_info(sbody) if skind == 2 else {"group": None, "hrr": False, "suite": "", "version": "",
                                                   "psk_accepted": False}
        rows.append({"sni": sni, "server_port": dport,
                     "client_offers_pq_keyshare": any(g in PQ for g in shares),
                     "client_supports_pq_group": any(g in PQ for g in supported),
                     "client_keyshares": " ".join(map(name, shares)),
                     "server_selected": name(s["group"]) if s["group"] is not None else
                                        ("none (TLS1.2 or resumption)" if skind == 2 else "no ServerHello captured"),
                     "hello_retry": s["hrr"], "pq_negotiated": s["group"] in PQ,
                     "tls_version": s["version"], "cipher_suite": s["suite"],
                     "resumption_offered": psk_offered, "psk_modes": psk_modes, "resumption_accepted": s["psk_accepted"]})
    return rows

# ---------------- APK framework detection ----------------
FILE_MARKERS = {"Flutter": r"lib/[^/]+/libflutter\.so$", "React Native": r"(lib/[^/]+/libreactnativejni\.so|assets/index\.android\.bundle)$",
                "Cronet (bundled)": r"lib/[^/]+/libcronet[^/]*\.so$", "Unity": r"lib/[^/]+/libunity\.so$",
                ".NET / Xamarin / MAUI": r"lib/[^/]+/libmonodroid\.so$", "WebView hybrid": r"assets/(www|public)/index\.html$"}
DEX_MARKERS = {"OkHttp": b"Lokhttp3/", "Cronet API": b"Lorg/chromium/net/", "Conscrypt (bundled copy)": b"Lorg/conscrypt/",
               "Cordova": b"Lorg/apache/cordova/", "Capacitor": b"Lcom/getcapacitor/", "Ktor": b"Lio/ktor/client/"}

SIGNALS = {"spki_pins": rb"sha(?:1|256)/[A-Za-z0-9+/=]{28,64}",                  # pinning regex from IMC'22
           "rsa_cipher_strings": rb"RSA/(?:ECB|NONE)/[A-Za-z0-9-]*Padding",      # app-layer RSA encryption
           "pem_public_keys": rb"-----BEGIN (?:RSA )?PUBLIC KEY-----",
           "pem_certificates": rb"-----BEGIN CERTIFICATE-----"}

def apk_crypto_signals(path):
    """Static hints for G9 (pinning) and G6 (app-layer crypto). Counts in dex, assets and res/raw only;
    obfuscated or native-code usage is missed (lower bound). Decode network_security_config with apktool."""
    counts = dict.fromkeys(SIGNALS, 0)
    with zipfile.ZipFile(path) as z:
        names = z.namelist()
        for n in names:
            if re.fullmatch(r"classes\d*\.dex", n) or n.startswith(("assets/", "res/raw/")):
                data = z.read(n)
                for k, rx in SIGNALS.items(): counts[k] += len(re.findall(rx, data))
        counts["cert_files"] = sum(bool(re.search(r"\.(cer|crt|pem|der)$", n)) for n in names)
        counts["network_security_config"] = any("network_security_config" in n for n in names)
    return counts

def apk_frameworks(path):
    with zipfile.ZipFile(path) as z:
        names = z.namelist()
        found = [f for f, rx in FILE_MARKERS.items() if any(re.search(rx, n) for n in names)]
        dex = b"".join(z.read(n) for n in names if re.fullmatch(r"classes\d*\.dex", n))
    return found + [f for f, m in DEX_MARKERS.items() if m in dex] or ["plain Java/Kotlin (platform HttpURLConnection?)"]

# ---------------- handshake timing: PQ vs classic on the current network ----------------
def handshake_ms(host, n):
    import socket, ssl, time
    out = []
    for _ in range(n):
        with socket.create_connection((host, 443), timeout=10) as s:
            t0 = time.perf_counter()                                    # TCP connect excluded
            with ssl.create_default_context().wrap_socket(s, server_hostname=host):
                out.append((time.perf_counter() - t0) * 1000)
    return out

def timing(host, n=20):
    """Runs n handshakes per group in child processes (OpenSSL groups can only be set via OPENSSL_CONF)."""
    import json, os, statistics, subprocess, tempfile
    for group in ["X25519MLKEM768", "X25519"]:
        conf = ("openssl_conf = a\n[a]\nssl_conf = b\n[b]\nsystem_default = c\n[c]\nGroups = " + group + "\n")
        with tempfile.NamedTemporaryFile("w", suffix=".cnf", delete=False) as f: f.write(conf)
        r = subprocess.run([sys.executable, __file__, "_child_timing", host, str(n)], capture_output=True, text=True,
                           env=dict(os.environ, OPENSSL_CONF=f.name))
        os.unlink(f.name)
        ms = json.loads(r.stdout) if r.returncode == 0 else None
        print(f"{host} {group:<15} " + (f"median {statistics.median(ms):6.1f} ms   "
              f"p90 {sorted(ms)[int(0.9 * (len(ms) - 1))]:6.1f} ms   (n={len(ms)})" if ms else "FAILED (server does not support it?)"))

# ---------------- shortcuts: can ONE quantum run decrypt MANY recorded sessions? ----------------
def server_hello(host):
    import socket, ssl
    inc, out = ssl.MemoryBIO(), ssl.MemoryBIO()
    tls = ssl.create_default_context().wrap_bio(inc, out, server_hostname=host)
    try: tls.do_handshake()
    except ssl.SSLWantReadError: pass
    buf = b""
    try:
        with socket.create_connection((host, 443), timeout=10) as s:
            s.sendall(out.read())
            while (hs := first_handshake(buf))[0] is None:
                if not (chunk := s.recv(4096)): return None
                buf += chunk
    except OSError: return None
    return hs[1] if hs[0] == 2 else None

def shortcuts(host, n=5):
    """Same server key share twice => one Shor run breaks all those sessions. RSA key transport accepted =>
    one Shor run on the certificate key breaks every session that used it (no forward secrecy)."""
    import socket, ssl
    shares = []
    for _ in range(n):
        b = server_hello(host)
        ext = hello_extensions(2, b)[1] if b else {}
        if len(ext.get(51, b"")) > 4: shares.append((name(u16(ext[51], 0)), ext[51][-32:]))   # last 32 B = X25519 part
    ctx = ssl.create_default_context(); ctx.maximum_version = ssl.TLSVersion.TLSv1_2; ctx.set_ciphers("kRSA")
    try:
        with socket.create_connection((host, 443), timeout=10) as s, ctx.wrap_socket(s, server_hostname=host) as t:
            rsa = "ACCEPTED " + t.cipher()[0]
    except OSError as e: rsa = "refused (" + type(e).__name__ + ")"
    groups = sorted({g for g, _ in shares})
    print(f"{host}: groups={groups} distinct_key_shares={len({k for _, k in shares})}/{len(shares)} rsa_key_transport={rsa}")

# ---------------- analysis: 2x2 per app, Wilson CI, McNemar ----------------
def wilson(k, n, z=1.96):
    if n == 0: return (0.0, 0.0)
    p = k / n
    mid, half = p + z * z / (2 * n), z * (p * (1 - p) / n + z * z / (4 * n * n)) ** 0.5
    return ((mid - half) / (1 + z * z / n), (mid + half) / (1 + z * z / n))

def mcnemar_exact(b, c):
    from math import comb
    n = b + c
    return 1.0 if n == 0 else min(1.0, 2 * sum(comb(n, k) for k in range(min(b, c) + 1)) / 2 ** n)

def analyze(conn_path, servers_path=None):
    import csv
    truthy = lambda v: str(v).strip().lower() in ("true", "yes", "ok", "1")
    rows = [r for r in csv.DictReader(open(conn_path, newline="")) if truthy(r.get("first_party", "yes"))]
    server_ok = {}
    if servers_path:
        for r in csv.DictReader(open(servers_path, newline="")): server_ok[r["domain"]] = truthy(r["pq_hybrid_handshake"])
    k = sum(truthy(r["pq_negotiated"]) for r in rows)
    lo, hi = wilson(k, len(rows))
    print(f"first-party connections with PQ negotiated: {k}/{len(rows)} = {k / max(len(rows), 1):.1%} "
          f"(95% CI {lo:.1%}-{hi:.1%})")
    cells, offers = {}, {}
    for (app, dev) in sorted({(r["app"], r["device"]) for r in rows}):
        rs = [r for r in rows if r["app"] == app and r["device"] == dev]
        c = any(truthy(r["client_offers_pq_keyshare"]) for r in rs)
        s = any(truthy(r["pq_negotiated"]) or server_ok.get(r["sni"], False) for r in rs)
        cell = {(1, 1): "protected", (1, 0): "server bottleneck", (0, 1): "app-side bottleneck",
                (0, 0): "both missing"}[(int(c), int(s))]
        cells.setdefault(cell, []).append(f"{app}@{dev}")
        offers[(app, dev)] = c
        print(f"  {app:<20} {dev:<12} client_offers_pq={c!s:<5} server_accepts_pq={s!s:<5} -> {cell}")
    for cell, apps in cells.items(): print(f"{cell}: {len(apps)}")
    devices = sorted({d for _, d in offers})
    if len(devices) == 2:                                               # paired test: same apps on 2 phones
        a, b = devices
        pairs = [(offers[(x, a)], offers[(x, b)]) for x, d in offers if d == a and (x, b) in offers]
        only_a, only_b = sum(p and not q for p, q in pairs), sum(q and not p for p, q in pairs)
        print(f"McNemar ({a} vs {b}, {len(pairs)} apps): offers PQ only on {a}={only_a}, only on {b}={only_b}, "
              f"exact p={mcnemar_exact(only_a, only_b):.3f}")
    return cells

# ---------------- self-test (offline) ----------------
def _write_pcap(path, link, packets):
    with open(path, "wb") as f:
        f.write(struct.pack("<IHHiIII", 0xA1B2C3D4, 2, 4, 0, 0, 65535, link))
        for p in packets: f.write(struct.pack("<IIII", 0, 0, len(p), len(p)) + p)

def _tcp(sport, dport, seq, payload, flags=0x18):
    return struct.pack(">HHIIBBHHH", sport, dport, seq, 0, 5 << 4, flags, 65535, 0, 0) + payload

def _ipv4(src, dst, seg): return struct.pack(">BBHHHBBH4s4s", 0x45, 0, 20 + len(seg), 0, 0, 64, 6, 0, src, dst) + seg
def _ipv6(src, dst, seg): return struct.pack(">IHBB16s16s", 6 << 28, len(seg), 6, 64, src, dst) + seg

def _server_hello(group):
    ks = struct.pack(">HH", group, 32) + bytes(32)
    ext = struct.pack(">HHH", 43, 2, 0x0304) + struct.pack(">HH", 51, len(ks)) + ks
    body = b"\x03\x03" + bytes(32) + b"\x00" + b"\x13\x01\x00" + struct.pack(">H", len(ext)) + ext
    hs = b"\x02" + len(body).to_bytes(3, "big") + body
    return b"\x16\x03\x03" + struct.pack(">H", len(hs)) + hs

def selftest():
    import os, ssl, tempfile
    inc, out = ssl.MemoryBIO(), ssl.MemoryBIO()
    tls = ssl.create_default_context().wrap_bio(inc, out, server_hostname="api.example.com.bd")
    try: tls.do_handshake()
    except ssl.SSLWantReadError: pass
    ch = out.read()
    python_offers_pq = ssl.OPENSSL_VERSION_INFO >= (3, 5)
    c4, s4 = bytes([10, 0, 0, 2]), bytes([1, 1, 1, 1])
    eth = lambda ip: b"\x00" * 12 + b"\x08\x00" + ip
    half = len(ch) // 2
    pkts = [eth(_ipv4(c4, s4, _tcp(50000, 443, 1000, b"", 0x02))),                 # SYN
            eth(_ipv4(c4, s4, _tcp(50000, 443, 1001 + half, ch[half:]))),         # 2nd half arrives first
            eth(_ipv4(c4, s4, _tcp(50000, 443, 1001, ch[:half]))),
            eth(_ipv4(c4, s4, _tcp(50000, 443, 1001, ch[:half]))),                # retransmission
            eth(_ipv4(s4, c4, _tcp(443, 50000, 7000, _server_hello(0x11EC))))]
    d = tempfile.mkdtemp()
    p1, p2 = os.path.join(d, "v4.pcap"), os.path.join(d, "v6.pcap")
    _write_pcap(p1, 1, pkts)
    c6, s6 = bytes(15) + b"\x02", bytes(15) + b"\x01"
    _write_pcap(p2, 101, [_ipv6(c6, s6, _tcp(40000, 443, 5, ch)), _ipv6(s6, c6, _tcp(443, 40000, 9, _server_hello(0x001D)))])
    (r1,), (r2,) = pcap_report([p1]), pcap_report([p2])
    assert r1["sni"] == r2["sni"] == "api.example.com.bd"
    assert r1["client_offers_pq_keyshare"] == python_offers_pq
    assert r1["pq_negotiated"] and r1["server_selected"] == "X25519MLKEM768"
    assert not r2["pq_negotiated"] and r2["server_selected"] == "X25519"
    assert r1["cipher_suite"] == "AES_128_GCM" and r1["tls_version"] == "TLS1.3" and not r1["resumption_accepted"]
    apk = os.path.join(d, "fake.apk")
    with zipfile.ZipFile(apk, "w") as z:
        z.writestr("lib/arm64-v8a/libflutter.so", b"")
        z.writestr("classes.dex", b"...Lokhttp3/OkHttpClient;...sha256/AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA="
                                  b"...RSA/ECB/OAEPWithSHA-256AndMGF1Padding...")
        z.writestr("assets/server.pem", b"-----BEGIN PUBLIC KEY-----\nMIIB...\n-----END PUBLIC KEY-----\n")
        z.writestr("res/xml/network_security_config.xml", b"\x03\x00binary-xml")
    assert apk_frameworks(apk) == ["Flutter", "OkHttp"]
    assert apk_crypto_signals(apk) == {"spki_pins": 1, "rsa_cipher_strings": 1, "pem_public_keys": 1,
                                       "pem_certificates": 0, "cert_files": 1, "network_security_config": True}
    import csv, io, contextlib
    conn, srv = os.path.join(d, "conn.csv"), os.path.join(d, "servers.csv")
    with open(conn, "w", newline="") as f:
        w = csv.writer(f); w.writerow(["app", "device", "first_party", "sni", "client_offers_pq_keyshare", "pq_negotiated"])
        w.writerows([["A", "old", "yes", "a.bd", "True", "True"], ["A", "new", "yes", "a.bd", "True", "True"],
                     ["B", "old", "yes", "b.bd", "False", "False"], ["B", "new", "yes", "b.bd", "True", "False"],
                     ["C", "old", "yes", "c.bd", "True", "False"], ["C", "new", "no", "ads.com", "True", "True"]])
    with open(srv, "w", newline="") as f:
        f.write("domain,classic_handshake,pq_hybrid_handshake\nb.bd,ok,ok\nc.bd,ok,SSLError\n")
    with contextlib.redirect_stdout(io.StringIO()):
        cells = analyze(conn, srv)
    assert cells == {"protected": ["A@new", "A@old", "B@new"], "app-side bottleneck": ["B@old"],
                     "server bottleneck": ["C@old"]}
    lo, hi = wilson(0, 10); assert abs(lo) < 1e-12 and 0.27 < hi < 0.28          # known value 0.2775
    assert abs(mcnemar_exact(0, 5) - 0.0625) < 1e-12
    print("selftest passed (Python OpenSSL offers PQ key share:", python_offers_pq, ")")

if __name__ == "__main__":
    import glob
    cmd, args = (sys.argv[1], sys.argv[2:]) if len(sys.argv) > 1 else ("", [])
    if cmd in ("pcap", "apk"):                                   # expand captures\*.pcap even in cmd/PowerShell
        args = [p for a in args for p in (sorted(glob.glob(a)) or [a])]
    if cmd == "pcap":
        rows = pcap_report(args)
        cols = list(rows[0]) if rows else []
        print(",".join(cols))
        for r in rows: print(",".join(str(r[c]) for c in cols))
    elif cmd == "apk":
        for a in args: print(f"{a}: frameworks={', '.join(apk_frameworks(a))}; signals={apk_crypto_signals(a)}")
    elif cmd == "analyze":
        analyze(args[0], args[1] if len(args) > 1 else None)
    elif cmd == "timing":
        timing(args[0], int(args[1]) if len(args) > 1 else 20)
    elif cmd == "shortcuts":
        for h in args: shortcuts(h)
    elif cmd == "_child_timing":
        import json; print(json.dumps(handshake_ms(args[0], int(args[1]))))
    elif cmd == "selftest":
        selftest()
    else:
        print(__doc__)
