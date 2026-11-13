"""Sistem pakar hama dan penyakit cabai - Forward Chaining.
Jalankan interaktif : python main.py
Jalankan non-interaktif (untuk uji): python main.py --ya "bercak keperakan pada daun muda,daun keriting"
"""
import json
import sys


def muat_kb(path="kb_cabai.json"):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def syarat_terpenuhi(aturan, memori):
    """mode 'dan' = semua syarat ada di memori, 'atau' = salah satu cukup."""
    ada = [s in memori for s in aturan["jika"]]
    return all(ada) if aturan["mode"] == "dan" else any(ada)


def forward_chaining(kb, fakta_awal):
    """Kembalikan (memori, asal, log).
    asal[fakta] = aturan yang menghasilkannya (bahan 'alasan')."""
    memori = set(fakta_awal)
    asal = {}
    log = []
    siklus = 0
    while True:
        siklus += 1
        cocok = [r for r in kb["aturan"]
                 if syarat_terpenuhi(r, memori) and r["maka"] not in memori]
        if not cocok:
            log.append(f"Siklus {siklus}: tidak ada aturan baru, berhenti")
            break
        r = cocok[0]                      # ambil aturan pertama
        memori.add(r["maka"])
        asal[r["maka"]] = r
        log.append(f"Siklus {siklus}: {r['id']} -> {r['maka']}")
    return memori, asal, log


def fakta_dasar(kb):
    """Fakta yang tidak pernah jadi hasil aturan -> ditanyakan ke user."""
    hasil = {r["maka"] for r in kb["aturan"]}
    urut = []
    for r in kb["aturan"]:
        for s in r["jika"]:
            if s not in hasil and s not in urut:
                urut.append(s)
    return urut


def alasan(fakta, memori, asal, indent=0):
    """Telusuri mundur dari sebuah kesimpulan sampai ke fakta awal."""
    r = asal[fakta]
    # hanya syarat yang benar-benar ada di memori yang dicatat sebagai alasan
    dipakai = [s for s in r["jika"] if s in memori]
    baris = [" " * indent + f"{fakta} <- {r['id']} ({', '.join(dipakai)}) [{r['sumber']}]"]
    for s in dipakai:
        if s in asal:
            baris += alasan(s, memori, asal, indent + 2)
    return baris


def tampilkan_hasil(kb, fakta_awal, memori, asal, log):
    print("\nFakta awal:", ", ".join(fakta_awal) if fakta_awal else "(tidak ada)")
    print()
    print("\n".join(log))
    final = [k for k in kb["kesimpulan"] if k in memori]
    print()
    if not final:
        print("Kesimpulan: tidak ada kesimpulan yang dapat ditarik dari fakta tersebut")
    else:
        print("Kesimpulan:")
        for k in final:
            print(f"  - {k}")
        print("Alasan:")
        for k in final:
            print("\n".join(alasan(k, memori, asal, 2)))
    print("\nCatatan:", kb["batas"])
    print("\nSumber:")
    for kode, teks in kb["sumber"].items():
        print(f"  {kode}: {teks}")


def tanya_user(kb):
    fakta = []
    print(kb["judul"])
    print("Jawab y/t.")
    for i, f in enumerate(fakta_dasar(kb), 1):
        while True:
            j = input(f"{i}. Apakah {f}? (y/t) > ").strip().lower()
            if j in ("y", "t"):
                break
            print("   Jawab dengan y atau t.")
        if j == "y":
            fakta.append(f)
    return fakta


def main():
    kb = muat_kb()
    if "--ya" in sys.argv:
        teks = sys.argv[sys.argv.index("--ya") + 1]
        fakta = [x.strip() for x in teks.split(",") if x.strip()]
        valid = set(fakta_dasar(kb))
        salah = [x for x in fakta if x not in valid]
        if salah:
            sys.exit(f"Fakta tidak dikenal: {salah}")
    else:
        fakta = tanya_user(kb)
    memori, asal, log = forward_chaining(kb, fakta)
    tampilkan_hasil(kb, fakta, memori, asal, log)


if __name__ == "__main__":
    main()