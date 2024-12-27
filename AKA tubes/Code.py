from collections import defaultdict
import heapq
import math

class Node:
    def __init__(self, name, lat, lon):
        self.name = name
        self.lat = lat  # latitude
        self.lon = lon  # longitude
        
class Graph:
    def __init__(self):
        self.nodes = {}  # Menyimpan node
        self.edges = defaultdict(list)  # Menyimpan edge dan bobot
        self.distances = {}  # Menyimpan jarak antar node
        
    def add_node(self, name, lat, lon):
        """Menambahkan node baru ke graph"""
        self.nodes[name] = Node(name, lat, lon)
        
    def add_edge(self, from_node, to_node, distance=None, bidirectional=True):
        """Menambahkan edge antara dua node"""
        if distance is None:
            # Hitung jarak berdasarkan koordinat geografis
            distance = self.calculate_distance(
                self.nodes[from_node].lat, 
                self.nodes[from_node].lon,
                self.nodes[to_node].lat, 
                self.nodes[to_node].lon
            )
            
        self.edges[from_node].append((to_node, distance))
        self.distances[(from_node, to_node)] = distance
        
        if bidirectional:
            self.edges[to_node].append((from_node, distance))
            self.distances[(to_node, from_node)] = distance
            
    def calculate_distance(self, lat1, lon1, lat2, lon2):
        """Menghitung jarak antara dua titik menggunakan formula Haversine"""
        R = 6371  # radius bumi dalam kilometer
        
        lat1_rad = math.radians(lat1)
        lon1_rad = math.radians(lon1)
        lat2_rad = math.radians(lat2)
        lon2_rad = math.radians(lon2)
        
        dlat = lat2_rad - lat1_rad
        dlon = lon2_rad - lon1_rad
        
        a = math.sin(dlat/2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon/2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - min(a, 1)))  # Memastikan a tidak lebih dari 1
        
        distance = R * c
        return distance
        
    def dijkstra(self, initial):
        """Implementasi algoritma Dijkstra untuk mencari rute terpendek"""
        distances = {node: float('infinity') for node in self.nodes}
        distances[initial] = 0
        pq = [(0, initial)]
        previous = {node: None for node in self.nodes}
        
        while pq:
            current_distance, current_node = heapq.heappop(pq)
            
            # Jika jarak yang ditemukan lebih besar dari yang sudah ada, skip
            if current_distance > distances[current_node]:
                continue
                
            # Periksa semua tetangga dari node saat ini
            for neighbor, weight in self.edges[current_node]:
                distance = current_distance + weight
                
                # Jika ditemukan jarak yang lebih pendek, update
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    previous[neighbor] = current_node
                    heapq.heappush(pq, (distance, neighbor))
                    
        return distances, previous
        
    def get_shortest_path(self, initial, destination):
        """Mendapatkan rute terpendek antara dua titik"""
        distances, previous = self.dijkstra(initial)
        
        if distances[destination] == float('infinity'):
            return None, None
            
        path = []
        current_node = destination
        
        while current_node is not None:
            path.append(current_node)
            current_node = previous[current_node]
            
        path.reverse()
        
        return path, distances[destination]

# Contoh penggunaan
def main():
    # Inisialisasi graph
    g = Graph()
    
    # Menambahkan beberapa lokasi (node) dengan koordinat lat/lon
    g.add_node("Jakarta", -6.2088, 106.8456)
    g.add_node("Bandung", -6.9175, 107.6191)
    g.add_node("Semarang", -7.0051, 110.4381)
    g.add_node("Surabaya", -7.2575, 112.7521)
    g.add_node("Yogyakarta", -7.7956, 110.3695)
    
    # Menambahkan koneksi jalan (edge)
    g.add_edge("Jakarta", "Bandung")
    g.add_edge("Bandung", "Semarang")
    g.add_edge("Semarang", "Surabaya")
    g.add_edge("Bandung", "Yogyakarta")
    g.add_edge("Yogyakarta", "Surabaya")
    g.add_edge("Semarang", "Yogyakarta")
    
    # Mencari rute terpendek
    start = "Jakarta"
    end = "Surabaya"
    
    path, distance = g.get_shortest_path(start, end)
    
    if path:
        print(f"\nRute terpendek dari {start} ke {end}:")
        print(" -> ".join(path))
        print(f"Total jarak: {distance:.2f} km")
    else:
        print(f"Tidak ditemukan rute dari {start} ke {end}")

# Memastikan program dijalankan hanya jika file ini dieksekusi langsung
if __name__ == "__main__":
    main()
