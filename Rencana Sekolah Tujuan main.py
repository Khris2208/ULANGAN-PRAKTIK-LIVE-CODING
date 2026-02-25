import json
from pathlib import Path
from math import radians, sin, cos, sqrt, atan2
from tabulate import tabulate


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


def select_level() -> str:
    """Ask user to select their educational level"""
    levels = ["SD", "SMP", "SMA", "SMK"]
    print("\n=== Pilih Jenjang Pendidikan ===")
    for i, level in enumerate(levels, start=1):
        print(f"  {i}. {level}")
    while True:
        choice = input("Pilih nomor jenjang (1-4): ").strip()
        if choice.isdigit():
            idx = int(choice)
            if 1 <= idx <= len(levels):
                return levels[idx - 1]
        print("Pilihan tidak valid, coba lagi.")


def choose_from_examples(level: str = None):
    examples = [
        ("SMA 1 Kota", 2.3),
        ("SMA 2 Kota", 5.0),
        ("SMK Teknik", 7.8),
        ("SMA Favorit", 12.5),
    ]
    if level:
        # Filter examples by level
        filtered = []
        for name, dist in examples:
            if (level == "SMA" and name in ["SMA 1 Kota", "SMA 2 Kota", "SMA Favorit"]) or (level == "SMK" and name == "SMK Teknik"):
                filtered.append((name, dist))
        examples = filtered
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
            {"name": "SMA 1 Kota", "level": "SMA", "dist": 1.2, "lat": -6.2000, "lon": 106.8000, "min_score": 75, "programs": [{"name": "IPA", "min_score": 80}, {"name": "IPS", "min_score": 75}, {"name": "Bahasa", "min_score": 70}]},
            {"name": "SMP Harapan", "level": "SMP", "dist": 1.8, "lat": -6.2010, "lon": 106.8050, "min_score": 65, "programs": [{"name": "Program A", "min_score": 70}, {"name": "Program B", "min_score": 65}]},
            {"name": "SD Nusantara", "level": "SD", "dist": 0.9, "lat": -6.1990, "lon": 106.7980, "min_score": 50, "programs": [{"name": "Kelas Reguler", "min_score": 50}]},
        ],
        'B': [
            {"name": "SMA 2 Kota", "level": "SMA", "dist": 3.5, "lat": -6.2100, "lon": 106.8200, "min_score": 70, "programs": [{"name": "IPA", "min_score": 78}, {"name": "IPS", "min_score": 72}, {"name": "Bahasa", "min_score": 68}, {"name": "Seni", "min_score": 65}]},
            {"name": "SMK Kreatif", "level": "SMK", "dist": 4.2, "lat": -6.2150, "lon": 106.8300, "min_score": 68, "programs": [{"name": "Desain Grafis", "min_score": 72}, {"name": "Multimedia", "min_score": 68}, {"name": "Animasi", "min_score": 70}]},
            {"name": "SMA Negeri 3", "level": "SMA", "dist": 5.8, "lat": -6.2250, "lon": 106.8400, "min_score": 72, "programs": [{"name": "IPA", "min_score": 78}, {"name": "IPS", "min_score": 72}]},
        ],
        'C': [
            {"name": "SMA Favorit", "level": "SMA", "dist": 9.5, "lat": -6.2500, "lon": 106.8600, "min_score": 85, "programs": [{"name": "IPA Unggulan", "min_score": 88}, {"name": "IPS Unggulan", "min_score": 85}]},
            {"name": "SMK Teknik", "level": "SMK", "dist": 12.0, "lat": -6.2700, "lon": 106.8800, "min_score": 80, "programs": [{"name": "Teknik Mesin", "min_score": 82}, {"name": "Teknik Otomotif", "min_score": 80}, {"name": "Teknik Elektronika", "min_score": 85}]},
            {"name": "SMA Unggulan", "level": "SMA", "dist": 18.3, "lat": -6.3000, "lon": 106.9000, "min_score": 88, "programs": [{"name": "IPA Advanced", "min_score": 92}, {"name": "IPS Advanced", "min_score": 90}, {"name": "STEM", "min_score": 94}]},
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


def filter_schools_by_score(recs_data: dict, min_score: float, level: str = None) -> list:
    """Filter all schools from recs_data where user_score >= min_score requirement and matches level"""
    matching = []
    for zone_key in ['A', 'B', 'C']:
        for school in recs_data.get(zone_key, []):
            if isinstance(school, dict):
                school_level = school.get('level', '')
                req_score = school.get('min_score', 0)
                if min_score >= req_score and (level is None or school_level == level):
                    matching.append({
                        'name': school.get('name'),
                        'level': school_level,
                        'dist': school.get('dist'),
                        'min_score': req_score,
                        'zone': zone_key,
                        'lat': school.get('lat'),
                        'lon': school.get('lon'),
                        'programs': school.get('programs', [])
                    })
    return sorted(matching, key=lambda x: x.get('min_score', 0), reverse=True)


def select_program(school: dict) -> dict | None:
    """Allow user to select a program/major from available options; returns {name, min_score}"""
    programs = school.get('programs', [])
    if not programs:
        return None
    if len(programs) == 1:
        prog = programs[0]
        if isinstance(prog, dict):
            return prog
        return {"name": prog, "min_score": school.get('min_score', '-')}
    
    print(f"\nProgram/Jurusan yang tersedia di {school.get('name')}:")
    
    # Prepare table data
    table_data = []
    for i, prog in enumerate(programs, start=1):
        if isinstance(prog, dict):
            table_data.append([i, prog.get('name', ''), prog.get('min_score', '-')])
        else:
            table_data.append([i, prog, school.get('min_score', '-')])
    
    headers = ["No", "Program/Jurusan", "Nilai Min"]
    print(tabulate(table_data, headers=headers, tablefmt="grid"))
    
    while True:
        sel = input('\nPilih nomor program/jurusan: ').strip()
        if sel.isdigit():
            si = int(sel)
            if 1 <= si <= len(programs):
                prog = programs[si - 1]
                if isinstance(prog, dict):
                    return prog
                return {"name": prog, "min_score": school.get('min_score', '-')}
        print('Pilihan tidak valid.')


def recommend_by_score(recs_data: dict, level: str = None) -> None:
    """Show school recommendations based on user's input score and level"""
    print('\n--- Mode: Rekomendasi Sekolah Berdasarkan Nilai ---')
    while True:
        try:
            user_score = float(input('Masukkan nilai Anda (0-100): ').strip())
            if 0 <= user_score <= 100:
                break
            print('Nilai harus antara 0-100.')
        except ValueError:
            print('Masukkan angka yang valid.')
    
    matching = filter_schools_by_score(recs_data, user_score, level)
    
    if not matching:
        level_str = f" untuk jenjang {level}" if level else ""
        print(f'\nSayang, tidak ada sekolah yang dapat Anda masuki dengan nilai {user_score}{level_str}.')
        print('Cobalah meningkatkan nilai Anda atau cari sekolah lain.')
        return
    
    print(f'\nSekolah yang dapat Anda masuki dengan nilai {user_score}:')
    
    # Prepare table data
    table_data = []
    for i, school in enumerate(matching, start=1):
        table_data.append([
            i,
            school.get('name', ''),
            school.get('level', '?'),
            school.get('zone', '?'),
            school.get('dist', '?'),
            school.get('min_score', '?')
        ])
    
    headers = ["No", "Sekolah", "Jenjang", "Zona", "Jarak (km)", "Nilai Min"]
    print(tabulate(table_data, headers=headers, tablefmt="grid"))
    
    # allow user to select one for details
    while True:
        sel = input('\nPilih nomor sekolah untuk detail lebih lanjut (0 untuk kembali): ').strip()
        if sel == '0':
            break
        if sel.isdigit():
            si = int(sel)
            if 1 <= si <= len(matching):
                selected = matching[si - 1]
                print(f"\nSekolah: {selected['name']}")
                print(f"Jenjang: {selected.get('level', '?')}")
                print(f"Zona: {selected['zone']}")
                print(f"Jarak (perkiraan): {selected['dist']} km")
                print(f"Nilai minimal untuk masuk: {selected['min_score']}")
                if 'lat' in selected and 'lon' in selected:
                    print(f"Koordinat: ({selected['lat']}, {selected['lon']})")
                # Show programs if available
                if 'programs' in selected and selected['programs']:
                    print("\nProgram/Jurusan tersedia:")
                    prog_table = []
                    for prog in selected['programs']:
                        if isinstance(prog, dict):
                            pname = prog.get('name', 'Program')
                            pscore = prog.get('min_score', '-')
                            prog_table.append([pname, pscore])
                        else:
                            prog_table.append([prog, '-'])
                    
                    headers_prog = ["Program/Jurusan", "Nilai Min"]
                    print(tabulate(prog_table, headers=headers_prog, tablefmt="grid"))
                continue
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
    
    # Select user's educational level
    user_level = select_level()
    print(f"\n✓ Jenjang terpilih: {user_level}")
    
    # show main menu
    while True:
        print('\n=== MENU UTAMA ===')
        print('1. Hitung jarak & rekomendasi (dengan input jarak)')
        print('2. Lihat rekomendasi sekolah berdasarkan nilai Anda')
        print('3. Ubah jenjang pendidikan')
        print('4. Keluar')
        menu_choice = input('Pilih menu (1/2/3/4): ').strip()
        if menu_choice == '1':
            break
        elif menu_choice == '2':
            recommend_by_score(recs_data, user_level)
            continue
        elif menu_choice == '3':
            user_level = select_level()
            print(f"\n✓ Jenjang terpilih: {user_level}")
            continue
        elif menu_choice == '4':
            print('Terima kasih — semoga membantu!')
            return
        else:
            print('Pilihan tidak valid.')
            continue
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
        name, dist = choose_from_examples(user_level)
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

        # Try to find school in recs_data and get programs
        selected_program = None
        school_obj = None
        for lst in recs_data.values():
            for item in lst:
                iname = item.get('name') if isinstance(item, dict) else item[0]
                if iname == name:
                    school_obj = item
                    break
            if school_obj:
                break
        
        if school_obj and isinstance(school_obj, dict):
            selected_program = select_program(school_obj)

        # rekomendasi sekolah berdasarkan zona (dimuat dari recommendations.json)
        zkey = zone_key(dist)
        zrecs = recs_data.get(zkey, [])
        # Filter recommendations by user's level
        zrecs = [s for s in zrecs if isinstance(s, dict) and s.get('level') == user_level]
        if zrecs:
            print(f"\nRekomendasi sekolah untuk zona ini (Jenjang {user_level}):")
            
            # Prepare table data
            zrecs_table = []
            for i, item in enumerate(zrecs, start=1):
                rname = item.get('name') if isinstance(item, dict) else item[0]
                rdist = item.get('dist') if isinstance(item, dict) else item[1]
                rlevel = item.get('level', '?')
                rmin = item.get('min_score', '-')
                zrecs_table.append([i, rname, rlevel, rdist, rmin])
            
            headers_zrec = ["No", "Sekolah", "Jenjang", "Jarak (km)", "Nilai Min"]
            print(tabulate(zrecs_table, headers=headers_zrec, tablefmt="grid"))

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
                        print(f"Memilih rekomendasi: {name} — {dist} km (Perkiraan nilai minimal: {chosen.get('min_score','-')})")
                        break
                print("Pilihan tidak valid, masukkan angka yang sesuai.")

        print("\nPilihan alat transportasi yang tersedia:")
        
        # Prepare table data for transportation
        trans_table = []
        for k, (label, speed) in transports.items():
            trans_table.append([k, label, f"{speed} km/jam"])
        
        headers_trans = ["Nomor", "Transportasi", "Kecepatan"]
        print(tabulate(trans_table, headers=headers_trans, tablefmt="grid"))

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
        if selected_program:
            if isinstance(selected_program, dict):
                prog_name = selected_program.get('name', 'Program')
                prog_score = selected_program.get('min_score', '-')
                print(f"Program/Jurusan: {prog_name} (Nilai min: {prog_score})")
            else:
                print(f"Program/Jurusan: {selected_program}")

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
