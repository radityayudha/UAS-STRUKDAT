import heapq        # Untuk implementasi priority queue pada algoritma Dijkstra
import math         # Untuk menggunakan konstanta tak hingga (infinity)
import itertools    # Untuk menghasilkan semua permutasi rute dalam TSP brute-force

# =============================== #
# 1. Representasi Graph (Peta Kota)
# =============================== #

# raw_graph menyimpan daftar kota dan tetangganya beserta jarak antar kota (dalam kilometer).
# Format: 'kota': {'tetangga1': jarak, 'tetangga2': jarak, ...}
raw_graph = {
    'surabaya': {'pasuruan': 62, 'sidoarjo': 26, 'mojokerto': 52, 'malang': 94.6, 'probolinggo': 101},
    'pasuruan': {'surabaya': 62, 'sidoarjo': 61, 'kediri': 110, 'malang': 45, 'probolinggo': 50},
    'sidoarjo': {'surabaya': 26, 'pasuruan': 61, 'mojokerto': 51.3, 'malang': 67.7},
    'kediri': {'pasuruan': 110, 'mojokerto': 80},
    'mojokerto': {'surabaya': 52, 'sidoarjo': 51.3, 'kediri': 80, 'tulungagung': 110},
    'tulungagung': {'mojokerto': 110, 'blitar': 29.2},
    'blitar': {'tulungagung': 29.2, 'madiun': 134},
    'madiun': {'blitar': 134, 'malang': 234},
    'malang': {'surabaya': 94.6, 'pasuruan': 45, 'sidoarjo': 67.7, 'madiun': 234, 'probolinggo': 80},
    'probolinggo': {'surabaya': 101, 'pasuruan': 50, 'malang': 80}
}

# Konversi raw_graph ke bentuk adjacency list menggunakan list of tuples.
# Format baru: 'kota': [('tetangga1', jarak), ('tetangga2', jarak), ...]
graph = {}
for src in raw_graph:
    for dst in raw_graph[src]:
        graph.setdefault(src, []).append((dst, raw_graph[src][dst]))


# ===================================================== #
# 2. Fungsi Dijkstra: Mencari Jalur Terpendek antar Dua Kota
# ===================================================== #

def dijkstra(graph, start, end):
    """
    Menggunakan algoritma Dijkstra untuk mencari jalur terpendek dari kota 'start' ke kota 'end'.
    Mengembalikan: path (daftar kota yang dilalui), total_jarak.
    """
    queue = [(0, start, [])]  # Priority queue berisi tuple (total_jarak, kota_saat_ini, jalur_sementara)
    visited = set()           # Menyimpan kota yang sudah dikunjungi agar tidak diulang

    while queue:
        cost, node, path = heapq.heappop(queue)  # Ambil elemen dengan total jarak terkecil dari queue
        if node in visited:
            continue
        visited.add(node)
        path = path + [node]  # Tambahkan node saat ini ke dalam jalur
 
        if node == end:
            return path, cost  # Jika sudah sampai ke tujuan, kembalikan jalur dan jaraknya

        # Periksa semua tetangga kota saat ini
        for neighbor, weight in graph.get(node, []):
            if neighbor not in visited:
                heapq.heappush(queue, (cost + weight, neighbor, path))  # Tambahkan ke queue

    return None, math.inf  # Jika tidak ada jalur, kembalikan None dan tak hingga


# ================================================================= #
# 3. Fungsi total_distance: Menghitung Total Jarak dari Suatu Rute
# ================================================================= #

def total_distance(route, graph):
    """
    Menghitung total jarak dari rute tertentu yang diberikan sebagai list kota.
    Rute tidak perlu kembali ke kota asal (seperti TSP tanpa kembali).
    """
    distance = 0
    for i in range(len(route) - 1):
        src = route[i]
        dst = route[i + 1]

        # Cek apakah dst adalah tetangga langsung dari src
        for neighbor, weight in graph[src]:
            if neighbor == dst:
                distance += weight
                break
        else:
            # Jika tidak ditemukan jalur langsung, maka rute tidak valid
            return math.inf
    return distance


# =========================================================================== #
# 4. Fungsi tsp_brute_force: Menyelesaikan TSP (Tanpa Kembali ke Kota Awal)
# =========================================================================== #

def tsp_brute_force(graph):
    """
    Menyelesaikan Travelling Salesman Problem (TSP) secara brute-force:
    Mencari rute terpendek untuk mengunjungi semua kota satu kali.
    Tidak perlu kembali ke kota asal.
    """
    cities = list(graph.keys())     # Daftar semua kota
    start = cities[0]               # Kota pertama dijadikan kota awal
    best_route = None              # Untuk menyimpan rute terbaik
    min_dist = math.inf           # Inisialisasi jarak minimum tak hingga

    # Lakukan permutasi untuk semua kota selain kota awal
    for perm in itertools.permutations(cities[1:]):
        route = [start] + list(perm)           # Gabungkan kota awal dengan permutasi
        dist = total_distance(route, graph)    # Hitung total jarak dari rute tersebut
        if dist < min_dist:                    # Simpan jika ditemukan rute lebih pendek
            min_dist = dist
            best_route = route

    return best_route, min_dist


# ======================================= #
# 5. Interaksi Pengguna melalui Terminal
# ======================================= #

# Tampilkan semua kota yang tersedia untuk dipilih
print("📍 Daftar Kota Tersedia:")
for city in sorted(graph.keys()):
    print("-", city)

# Input dari pengguna: kota asal dan kota tujuan
start_city = input("\nMasukkan kota asal: ").strip().lower()
end_city = input("Masukkan kota tujuan: ").strip().lower()

# Validasi input: apakah kota tersebut ada dalam graph?
if start_city not in graph or end_city not in graph:
    print("❌ Salah satu kota tidak ditemukan.")
else:
    # Jalankan algoritma Dijkstra untuk menemukan jalur terpendek
    path, dist = dijkstra(graph, start_city, end_city)
    if path:
        print("\n✅ Jalur Terpendek (Dijkstra):")
        print(" → ".join(path))  # Tampilkan jalur dalam format kota1 → kota2 → ...
        print(f"📏 Total Jarak: {dist:.2f} km")
    else:
        print("❌ Tidak ditemukan jalur antar kota.")

# Jalankan algoritma TSP menggunakan brute-force
print("\n🔁 Menjalankan Brute-force TSP (tanpa kembali ke kota asal)...")
best_route, tsp_dist = tsp_brute_force(graph)
if best_route:
    print("\n🏆 Rute TSP Optimal:")
    print(" → ".join(best_route))                # Tampilkan urutan kota
    print(f"📏 Total Jarak TSP: {tsp_dist:.2f} km")  # Tampilkan total jarak
else:
    print("❌ Tidak ditemukan rute TSP yang valid.")
