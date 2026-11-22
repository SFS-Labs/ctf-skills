# Verifikation — echte Laeufe (Stand 2026-11-21)

Ziel: `corpora/verify/Vulnerable.sol` — Vault mit Reentrancy, `tx.origin`-Sweep und unchecked Low-Level-Call.
Kein `--help`-Test, sondern Findings an einem Programm mit bekannten Fehlern.

| Layer | Werkzeug | Ergebnis |
|---|---|---|
| L1 | `solc-select` / `crytic-compile` | solc **0.8.28** gepinnt, AST/ABI gebaut |
| L1 | `surya` | Contract-Map erzeugt (deposit, withdraw, sweep, forceSend) |
| L2 | `slither` | `reentrancy-eth` in `Vault.withdraw()` + Arbitrary-Send in `Vault.sweep()` |
| L4 | `mythril` | SWC-115 *Dependence on tx.origin* in `Vault` |
| L3 | `echidna` | Counterexample: `deposit → sweep` bricht `echidna_solvent` (Reason `ReturnFalse`) |
| L3 | `medusa` | 36.995 Calls, Coverage-Report erzeugt — flaggt die Invariante **nicht** |
| PoC | `forge` | 3/3 Tests grün: Invariante hält anfangs, Sweep bricht sie, Reentrancy drainiert den Vault |

## Divergenz-Befund (Emergenz-Regel 3)

Echidna findet den Bruch, Medusa nicht — bei identischer Quelle und identischen Sendern.
Damit ist belegt, warum ein einzelnes Tool kein „sauber" liefern darf: Medusa allein hätte hier
einen Fehlalarm-negativen Befund produziert. Die Regel „zwei Signale aus verschiedenen Schichten"
ist damit empirisch, nicht nur behauptet.

## Was zusätzlich nachgewiesen wurde

- `forge test` läuft ohne forge-std (eigene `Vm`-Interface-Deklaration für `prank(sender, origin)`).
- Reentrancy-Test korrigiert: die Solvenz-Invariante bleibt scheinbar wahr, weil `totalDeposits`
  mit sinkt — der Diebstahl zeigt sich nur am Guthaben (`balance <= 1 ether`). Genau diese
  Falle ist der Grund, warum Counterexample + PoC zusammen geprüft werden müssen.
- `exploitdb`: GitHub-Repo ist **archiviert und geleert** (nur noch README); Daten kommen vom
  offiziellen Nachfolger `gitlab.com/exploit-database/exploitdb` — 10,2 MB Exploit-CSV + 220 KB Shellcodes.

## Grenzen (ehrlich, nicht behoben)

| Skill | Grund |
|---|---|
| `cryo` | `openssl-sys` braucht `libssl-dev` (Root); kein Release-Asset vorhanden |
| `diffusc` | hängt an einem git-Fork von slither; `git` fehlt, Elevation nicht bestätigt |
| `daedaluzz` | ist **Go** (nicht Python); keine Go-Toolchain installiert |
| `attacknet`, `eth-security-toolbox`, `cloudexec`, `paradigm-ctf-infra` | brauchen Docker; Rezepte liegen in `recipes/` |
| `ida-evm`, `ethersplay` | IDA nicht installiert; Bytecode-Schicht läuft über `etheno`/`evmasm`/`evm-cfg-builder` |
| Repo-Versionierung | kein `git` → Updates über `python3 bin/fetch` (authentifizierte Tarballs) |

## Nachtrag 2026-11-21: cryo, diffusc, daedaluzz lauffähig gemacht

Alle drei waren als "nicht lauffähig" dokumentiert. Die echten Ursachen waren andere als vermutet
und sind hier mit Beweis-Kommando festgehalten.

### daedaluzz — Go, nicht Python
`go.mod` sagt `go 1.15`, es ist ein Go-Programm (`main.go`, Deps logrus + urfave/cli).
Fix: Userspace-Go 1.23.4 nach `~/.local/opt` (kein Root), dann `go build` im vendor-Baum.
Rezept: `recipes/daedaluzz-build.sh`.

```
$ cd /tmp/proof-daedaluzz && daedaluzz        # exit=0
$ ls -l generated-maze.sol                     # 32560 bytes
$ solc --bin generated-maze.sol | grep -c '^======= '   # 1 Contract (Maze) kompiliert
```

### diffusc — git war nie das Laufzeitproblem
`setup.py` deklariert genau eine git-Abhängigkeit (`slither-analyzer@git+https://github.com/webthethird/slither.git@dev-diffusc-testing`).
Der Code ruft nirgends git auf (grep über alle `*.py`). Fix: Fork als codeload-Tarball installieren,
diffusc mit `--no-deps` dazu. Zwei Folgeprobleme mussten gelöst werden:

1. `pkg_resources.require("diffusc")` → VersionConflict wegen der git-URL in `Requires-Dist`
   → lokaler Patch: feste Version im `--version`-Zweig.
2. `solc_select` fragt `binaries.soliditylang.org` per urllib **ohne User-Agent** an → HTTP 403
   (sowohl `list.json` als auch der solc-Download via `urlretrieve`) → Patch mit UA-Header.

Zusätzlich: `forge` muss im PATH sein, sonst wählt crytic-compile das Foundry-Plugin
(`FileNotFoundError: 'forge'`), und der **Dateiname** bestimmt den Contract-Namen
(`VaultV1.sol` → Contract `Vault`; `VaultA.sol` → IndexError).
Rezept: `recipes/diffusc-setup.sh`.

```
$ diffusc /tmp/diffusc-src/VaultV1.sol /tmp/diffusc-src/VaultV2.sol -d /tmp/proof-diffusc
  * tainted_functions: ...
  * Fuzzing contract generated and written to /tmp/proof-diffusc/DiffFuzzUpgrades.sol
  * Echidna configuration file generated and written to /tmp/proof-diffusc/CryticConfig.yaml
My work here is done. Thanks for using me, have a nice day!
```

### cryo — kein Release-, sondern ein Header- und Compiler-Problem
Die Releases-API von `paradigmxyz/cryo` hat genau ein Release (`0.2.0`) **ohne Assets** — ein
fertiges Binary gibt es nicht, Selbstbau ist zwingend. Der Abbruch lag an zwei Dingen:

1. `openssl-sys` (über alloy/reqwest, native-tls) braucht Dev-Header. `libssl.so.3` ist vorhanden,
   `libssl-dev` nicht. `apt-get download libssl-dev` funktioniert **ohne Root**; mit `dpkg-deb -x`
   nach `~/.local/openssl-dev` entpacken und `OPENSSL_INCLUDE_DIR`/`OPENSSL_LIB_DIR` setzen.
   Wichtig: `opensslconf.h`/`configuration.h` liegen im Multiarch-Zweig
   (`usr/include/x86_64-linux-gnu/openssl/`) und müssen nach `usr/include/openssl/` kopiert werden.
2. Danach `ethnum 1.5.0`: `error[E0512]: cannot transmute between types of different sizes`
   auf rustc 1.100 → `cargo update -p ethnum` (1.5.3).

Rezept: `recipes/cryo-build.sh`.

```
$ cryo --version
cryo 0.3.2
$ cryo blocks --blocks 19000000 -r https://ethereum-rpc.publicnode.com -o /tmp/cryo-out
- blocks collected: 1
- rows written: 1
$ ls /tmp/cryo-out/*.parquet
ethereum__blocks__19000000_to_19000000.parquet      # 1 Row, Schema blocks
```

## Automatisierte Beweislaeufe — `bin/smoke` (2026-11-21)

Die Nachweise oben sind ab jetzt reproduzierbar statt einmalig: `bin/smoke` faehrt sie in
temporaeren Verzeichnissen und prueft die Artefakte **inhaltlich**, nicht nur auf Existenz.

| Werkzeug | Kommando (so ruft `bin/smoke` es auf) | inhaltliche Pruefung |
|---|---|---|
| `cryo` | `cryo blocks --blocks 19000000 -r <rpc> -o <tmp>/out` | Parquet per pyarrow gelesen: 1 Row, 8 Spalten, `block_number == 19000000` |
| `diffusc` | `diffusc <tmp>/VaultV1.sol <tmp>/VaultV2.sol -d <tmp>/out` | `DiffFuzzUpgrades.sol` enthaelt `contract`, `CryticConfig.yaml` nicht leer |
| `daedaluzz` | `daedaluzz` im leeren Verzeichnis | `generated-maze.sol` > 5 kB, `pragma solidity` + `contract`, mit `solc --bin` kompiliert |
| `push` | `bin/push --selftest` | sechs synthetische Lecks (dulwich-Erfolgszeile, URL-Userinfo, Bearer-Header, Query-Token) muessen redigiert sein; kein `LEAK` |

Fixtures liegen jetzt im Repo: `corpora/smoke/VaultV1.sol` / `VaultV2.sol` (vorher nur unter `/tmp`).
Ergebnis: `logs/smoke.json` (maschinenlesbar, nicht versioniert) und ein Block in `STATUS.md`,
den `bin/doctor` beim Neuschreiben erhaelt.

Beim Automatisieren gefunden und im Rezept vermerkt: diffusc bricht mit `IndexError` in
`slither_provider.py:155` ab, wenn der Pfad **keinen** Verzeichnis-Separator enthaelt
(`path.rsplit(os.sep, 1)[1]`) — also nie nackte Dateinamen uebergeben.

`bin/smoke` endet mit Exit 0, wenn kein Werkzeug `FAIL` ist. `SKIP` heisst: Umgebung fehlt
(Binary, `forge`, `solc` oder Netz) — kein bestandener Test, aber auch kein stilles Rot.
