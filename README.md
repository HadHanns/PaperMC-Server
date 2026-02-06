# PaperMC Server Control Hub (macOS)

Repo ini menyimpan seluruh skrip & GUI desktop bertema Minecraft untuk mengelola server PaperMC (Java) di macOS Apple Silicon, lengkap dengan dukungan Bedrock (Geyser/Floodgate) dan otomatisasi backup.

## Fitur Utama

1. **Start/Stop Server** – `start.sh` (Aikar flags + prompt aware), `stop` di console untuk shutdown bersih.
2. **GUI Minecraft (`server_gui.py`)**
   - Header ASCII + dekorasi leaf/torch/diamond
   - Tombol blok (Start, Stop, Auto Backup) dengan state jelas
   - Status chip & animasi hearts
   - Panel `Server Console` + `Backup Log`
3. **Backup**
   - `backup.sh` (manual, retensi 7 arsip)
   - `auto_backup.sh` (interval menit, bisa dijalankan via GUI)
4. **Geyser + Floodgate** siap pakai untuk pemain Bedrock
5. **Dokumentasi lengkap**: `SERVER_MANUAL.md`, `SETUP_GUIDE.md`

## Prasyarat
- macOS + Terminal
- Java 21 (`java -version`)
- `paper.jar` terbaru di root repo

## Struktur Direktori Penting

| Path | Keterangan |
| --- | --- |
| `start.sh` | Jalankan server PaperMC (Aikar flags, Java 21). |
| `server_gui.py` | GUI Tkinter bertema Minecraft (start/stop/log/auto backup). |
| `backup.sh` | Backup manual world + plugins. |
| `auto_backup.sh` | Script auto-backup (dipanggil GUI/cron/screen). |
| `plugins/` | Termasuk Geyser/Floodgate; tinggal tambah plugin lain. |
| `SERVER_MANUAL.md` | Operasional harian (port, whitelist, troubleshooting). |
| `SETUP_GUIDE.md` | Panduan first install PaperMC + Java di macOS. |

## Cara Menjalankan

### Terminal
```bash
./start.sh
# Ketik 'stop' untuk shutdown
```

### GUI Minecraft
```bash
python3 server_gui.py
```
Fitur GUI:
- Tombol **Start Server**, **Stop Server**, dan **Auto Backup**
- Panel log real-time + panel khusus *Auto Backup Log*
- Status chip + animasi hearts sesuai kondisi server

## Backup Ops
- **Manual**: `./backup.sh` (disarankan sebelum update plugin/reset world)
- **Auto**: `./auto_backup.sh 60` atau tombol Auto Backup di GUI (jalan `auto_backup.sh 60` dan tampilkan log)
- Output: folder `backups/` (retain 7 arsip terbaru)

## Dunia & Seed
1. Edit `server.properties` → `level-seed=<angka>` (boleh kosong)
2. Stop server → backup → hapus `world*`
3. Jalankan `./start.sh` untuk generate ulang

## Port Forwarding & Bedrock
- IP lokal: `ipconfig getifaddr en0`
- Forward: `25565 TCP/UDP` (Java) + `19132 UDP` (Bedrock/Geyser)
- IP publik: `curl ifconfig.me` atau pakai DDNS

## Git Workflow
```bash
git status
git add <file>
git commit -m "pesan"
git push origin master
```

## Referensi
- `SERVER_MANUAL.md` & `SETUP_GUIDE.md`
- PaperMC Docs – https://docs.papermc.io/
- GeyserMC – https://geysermc.org/

Selamat mengatur server PaperMC Anda! 🎮 Jika butuh fitur tambahan (plugin baru, penyesuaian GUI, otomatisasi extra), repo ini siap dikembangkan. 
