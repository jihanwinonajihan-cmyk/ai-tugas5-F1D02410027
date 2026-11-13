"""Uji otomatis lima kasus uji."""
from main import muat_kb, forward_chaining

kb = muat_kb()
kasus = [
    ("1", ["tanaman layu di siang hari", "tanaman segar kembali di sore hari"],
     {"layu fusarium"}),
    ("2", ["tanaman layu di siang hari", "layu berkembang cepat"],
     {"layu bakteri"}),
    ("3", ["bercak keperakan pada daun muda", "daun keriting"],
     {"serangan thrips", "penyakit virus keriting"}),
    ("4 (negatif)", ["daun keriting"], set()),
    ("5", ["bercak coklat kehitaman oval pada buah"], {"antraknosa"}),
]
for nama, fakta, harap in kasus:
    memori, _, _ = forward_chaining(kb, fakta)
    hasil = {k for k in kb["kesimpulan"] if k in memori}
    print(f"Kasus {nama}: {'LULUS' if hasil == harap else 'GAGAL'}  -> {sorted(hasil) or 'tidak ada'}")