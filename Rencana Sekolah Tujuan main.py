import json
from pathlib import Path
from math import radians, sin, cos, sqrt, atan2


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


def haversine(lat1, lon1, lat2, lon2):
    # return distance in kilometers between two lat/lon points
    R = 6371.0
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat / 2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c


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


def input_coord(prompt_lat: str, prompt_lon: str):
    while True:
        lat = input(prompt_lat).strip().replace(',', '.')
        lon = input(prompt_lon).strip().replace(',', '.')
        try:
            latf = float(lat)
            lonf = float(lon)
            return latf, lonf
        except ValueError:
            print("Masukkan angka untuk koordinat (mis. -6.2000 dan 106.8166).")


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
            {"name": "SMA 1 Kota", "dist": 1.2, "lat": -6.2000, "lon": 106.8000, "min_score": 75},
            {"name": "SMP Harapan", "dist": 1.8, "lat": -6.2010, "lon": 106.8050, "min_score": 65},
            {"name": "SD Nusantara", "dist": 0.9, "lat": -6.1990, "lon": 106.7980, "min_score": 50},
        ],
        'B': [
            {"name": "SMA 2 Kota", "dist": 3.5, "lat": -6.2100, "lon": 106.8200, "min_score": 70},
            {"name": "SMK Kreatif", "dist": 4.2, "lat": -6.2150, "lon": 106.8300, "min_score": 68},
            {"name": "SMA Negeri 3", "dist": 5.8, "lat": -6.2250, "lon": 106.8400, "min_score": 72},
        ],
        'C': [
            {"name": "SMA Favorit", "dist": 9.5, "lat": -6.2500, "lon": 106.8600, "min_score": 85},
            {"name": "SMK Teknik", "dist": 12.0, "lat": -6.2700, "lon": 106.8800, "min_score": 80},
            {"name": "SMA Unggulan", "dist": 18.3, "lat": -6.3000, "lon": 106.9000, "min_score": 88},
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
        for k in ['A', 'B', 'C']:
            if k not in data:
                data[k] = default[k]
        return data
    except Exception:
        return default


def load_homes(path: str = 'homes.json') -> list:
    p = Path(path)
    if not p.exists():
        try:
            p.write_text('[]')
        except Exception:
            pass
        return []
    try:
        data = json.loads(p.read_text())
        if isinstance(data, list):
            return data
        return []
    except Exception:
        return []


def save_homes(homes: list, path: str = 'homes.json') -> None:
    try:
        Path(path).write_text(json.dumps(homes, indent=2, ensure_ascii=False))
    except Exception:
        pass


def manage_homes() -> dict | None:
    homes = load_homes()
    while True:
        print('\nData alamat rumah tersimpan:')
        if homes:
            for i, h in enumerate(homes, start=1):
                print(f"  {i}. {h.get('name')} — ({h.get('lat')}, {h.get('lon')})")
        else:
            print('  (kosong)')
        print('  a. Tambah alamat baru')
        print('  0. Kembali')
        sel = input('Pilih alamat (nomor), atau pilih aksi: ').strip().lower()
        if sel == '0':
            return None
        if sel == 'a':
            name = input('Nama alamat (mis. Rumah Bapak): ').strip() or 'Alamat'
            lat, lon = input_coord('Latitude: ', 'Longitude: ')
            new = {'name': name, 'lat': lat, 'lon': lon}
            homes.append(new)
            save_homes(homes)
            print('Alamat tersimpan.')
            continue
        if sel.isdigit():
            si = int(sel)
            if 1 <= si <= len(homes):
                return homes[si - 1]
        print('Pilihan tidak valid.')


def main():
    transports = {
        "1": ("Jalan kaki", 5.0),
        "2": ("Sepeda", 15.0),
        "3": ("Motor", 40.0),
        "4": ("Mobil", 50.0),
        "5": ("Transportasi umum", 30.0),
    }

    recs_data = load_recommendations()

    print("Program Penentu Sekolah Tujuan — Hitung Jarak & Waktu Perjalanan")
    while True:
        # choose home mode
        print('\nSumber data rumah:')
        print('  1. Gunakan/kelola alamat rumah tersimpan (hitung jarak otomatis jika tersedia)')
        print('  2. Masukkan jarak/manual (seperti sebelumnya)')
        home = None
        mode = input('Pilih sumber (1/2): ').strip()
        if mode == '1':
            home = manage_homes()
        # proceed to school selection
        name, dist = choose_from_examples()
        if name is None:
            name = input("Masukkan nama sekolah tujuan: ").strip() or "Sekolah tujuan"
            if home is None:
                dist = input_distance("Masukkan jarak dari rumah ke sekolah (km): ")
            else:
                # ask if user has coordinates for school or wants to input manually
                has_coords = input('Apakah Anda memiliki koordinat sekolah? (y/n): ').strip().lower()
                if has_coords == 'y':
                    slat, slon = input_coord('Latitude sekolah: ', 'Longitude sekolah: ')
                    # compute distance from selected home
                    if home and 'lat' in home and 'lon' in home:
                        dist = round(haversine(home['lat'], home['lon'], slat, slon), 2)
                        print(f"Jarak terhitung: {dist} km")
                    else:
                        dist = input_distance("Masukkan jarak dari rumah ke sekolah (km): ")
                else:
                    dist = input_distance("Masukkan jarak dari rumah ke sekolah (km): ")
        else:
            # if a recommended school was picked from examples, see if it exists in recommendations data
            pass

        # if user selected a stored home and the chosen school exists in recs_data with coords, compute distance
        if home is not None:
            # try to find chosen school in recommendations
            found = None
            for lst in recs_data.values():
                for item in lst:
                    iname = item.get('name') if isinstance(item, dict) else item[0]
                    if iname == name:
                        found = item
                        break
                if found:
                    break
            if found and 'lat' in found and 'lon' in found and 'lat' in home and 'lon' in home:
                dist = round(haversine(home['lat'], home['lon'], found['lat'], found['lon']), 2)
                print(f"Jarak dihitung dari alamat terpilih: {dist} km")

        print(f"\nSekolah tujuan: {name}")
        print(f"Jarak: {dist} km")
        zone = classify_zone(dist)
        print(f"Zona sekolah berdasarkan jarak: {zone}")

        # rekomendasi sekolah berdasarkan zona (dimuat dari recommendations.json)
        zkey = zone_key(dist)
        zrecs = recs_data.get(zkey, [])
        if zrecs:
            print("\nRekomendasi sekolah untuk zona ini:")
            for i, item in enumerate(zrecs, start=1):
                rname = item.get('name') if isinstance(item, dict) else item[0]
                rdist = item.get('dist') if isinstance(item, dict) else item[1]
                print(f"  {i}. {rname} — {rdist} km (Perkiraan nilai minimal: {item.get('min_score','-')})")

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
                        # if chosen has coords and home is set, recompute dist
                        if isinstance(chosen, dict) and 'lat' in chosen and 'lon' in chosen and home and 'lat' in home and 'lon' in home:
                            dist = round(haversine(home['lat'], home['lon'], chosen['lat'], chosen['lon']), 2)
                        else:
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
