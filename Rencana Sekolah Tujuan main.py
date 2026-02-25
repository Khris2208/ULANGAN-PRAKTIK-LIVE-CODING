import json
from pathlib import Path


def format_time(hours: float) -> str:
    total_minutes = int(round(hours * 60))
    h = total_minutes // 60
    m = total_minutes % 60
    parts = []
    if h:
        parts.append(f"{h} jam")
    if m or not parts:
        parts.append(f"{m} menit")
    return " ".join(parts)


def choose_from_examples():
    examples = [
        ("SMA 1 Kota", 2.3),
        ("SMA 2 Kota", 5.0),
        ("SMK Teknik", 7.8),
        ("SMA Favorit", 12.5),
    ]
    print("Daftar contoh sekolah:")
    for i, (name, dist) in enumerate(examples, start=1):
        print(f"  {i}. {name} — {dist} km")
    print("  0. Masukkan sekolah lain / jarak sendiri")
    while True:
        choice = input("Pilih nomor sekolah (0 untuk input manual): ")
        if choice.isdigit():
            idx = int(choice)
            if idx == 0:
                return None, None
            if 1 <= idx <= len(examples):
                return examples[idx - 1]
        print("Pilihan tidak valid, coba lagi.")


def input_distance(prompt: str) -> float:
    while True:
        s = input(prompt).strip().replace(',', '.')
        try:
            d = float(s)
            if d < 0:
                print("Jarak tidak boleh negatif.")
                continue
            return d
        except ValueError:
            print("Masukkan angka untuk jarak (mis. 3.5).")


def classify_zone(distance: float) -> str:
    if distance <= 2.0:
        return "Zona A (Dekat)"
    if distance <= 6.0:
        return "Zona B (Sedang)"
    return "Zona C (Jauh)"


def zone_key(distance: float) -> str:
    if distance <= 2.0:
        return 'A'
    if distance <= 6.0:
        return 'B'
    return 'C'
def load_recommendations(path: str = 'recommendations.json') -> dict:
    p = Path(path)
    default = {
        'A': [
            {"name": "SMA 1 Kota", "dist": 1.2},
            {"name": "SMP Harapan", "dist": 1.8},
            {"name": "SD Nusantara", "dist": 0.9},
        ],
        'B': [
            {"name": "SMA 2 Kota", "dist": 3.5},
            {"name": "SMK Kreatif", "dist": 4.2},
            {"name": "SMA Negeri 3", "dist": 5.8},
        ],
        'C': [
            {"name": "SMA Favorit", "dist": 9.5},
            {"name": "SMK Teknik", "dist": 12.0},
            {"name": "SMA Unggulan", "dist": 18.3},
        ],
    }
    if not p.exists():
        try:
            p.write_text(json.dumps(default, indent=2, ensure_ascii=False))
        except Exception:
            pass
        return default
    try:
        data = json.loads(p.read_text())
        # normalize: ensure keys A/B/C present and convert items to dicts
        for k in ['A', 'B', 'C']:
            if k not in data:
                data[k] = default[k]
        return data
    except Exception:
        return default


def main():
    transports = {
        "1": ("Jalan kaki", 5.0),
        "2": ("Sepeda", 15.0),
        "3": ("Motor", 40.0),
        "4": ("Mobil", 50.0),
        "5": ("Transportasi umum", 30.0),
    }

    print("Program Penentu Sekolah Tujuan — Hitung Jarak & Waktu Perjalanan")
    while True:
        name, dist = choose_from_examples()
        if name is None:
            name = input("Masukkan nama sekolah tujuan: ").strip() or "Sekolah tujuan"
            dist = input_distance("Masukkan jarak dari rumah ke sekolah (km): ")

        print(f"\nSekolah tujuan: {name}")
        print(f"Jarak: {dist} km")
        zone = classify_zone(dist)
        print(f"Zona sekolah berdasarkan jarak: {zone}")

        # rekomendasi sekolah berdasarkan zona (dimuat dari recommendations.json)
        recs_data = load_recommendations()
        zkey = zone_key(dist)
        zrecs = recs_data.get(zkey, [])
        if zrecs:
            print("\nRekomendasi sekolah untuk zona ini:")
            for i, item in enumerate(zrecs, start=1):
                rname = item.get('name') if isinstance(item, dict) else item[0]
                rdist = item.get('dist') if isinstance(item, dict) else item[1]
                print(f"  {i}. {rname} — {rdist} km")

            # allow user to pick one of the recommendations as the chosen school
            while True:
                sel = input("Pilih nomor rekomendasi untuk digunakan sebagai sekolah tujuan (0 untuk tetap menggunakan input): ").strip()
                if sel.isdigit():
                    si = int(sel)
                    if si == 0:
                        break
                    if 1 <= si <= len(zrecs):
                        chosen = zrecs[si - 1]
                        name = chosen.get('name') if isinstance(chosen, dict) else chosen[0]
                        dist = chosen.get('dist') if isinstance(chosen, dict) else chosen[1]
                        print(f"Memilih rekomendasi: {name} — {dist} km")
                        break
                print("Pilihan tidak valid, masukkan angka yang sesuai.")

        print("\nPilihan alat transportasi yang tersedia:")
        for k, (label, speed) in transports.items():
            print(f"  {k}. {label} — {speed} km/jam")

        # show recommended options based on distance (simple heuristic)
        recs = []
        if dist <= 2.0:
            recs = ["1", "2"]  # walking or bicycle
        elif dist <= 6.0:
            recs = ["2", "3", "5"]
        else:
            recs = ["3", "4", "5"]

        rec_labels = ", ".join(transports[r][0] for r in recs)
        print(f"Rekomendasi alat transportasi (berdasarkan jarak): {rec_labels}")

        choice = input("Pilih nomor transportasi yang ingin dipakai: ").strip()
        if choice not in transports:
            print("Pilihan transportasi tidak valid, pilih salah satu nomor yang tersedia.")
            continue

        label, speed = transports[choice]
        hours = dist / speed if speed > 0 else float('inf')
        print(f"\nAnda memilih: {label}")
        print(f"Kecepatan rata-rata: {speed} km/jam")
        print(f"Perkiraan waktu perjalanan: {format_time(hours)}")

        # show fastest option
        best = min(transports.values(), key=lambda x: dist / x[1])
        best_time = dist / best[1]
        print(f"Waktu tercepat jika memilih {best[0]}: {format_time(best_time)}")

        again = input("\nIngin menghitung lagi? (y/n): ").strip().lower()
        if again != 'y':
            print("Terima kasih — semoga membantu!")
            break


if __name__ == '__main__':
    main()
