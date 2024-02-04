import threading
import time

class DirectionSemaphore:
    def __init__(self):
        self.mutex = threading.Lock()
        self.northbound_count = 0
        self.southbound_count = 0

    def wait(self, direction):
        with self.mutex:
            if direction == "Northbound":
                self.northbound_count += 1
                return True
            elif direction == "Southbound":
                self.southbound_count += 1
                return True

    def signal(self, direction):
        with self.mutex:
            if direction == "Northbound":
                self.northbound_count -= 1
            elif direction == "Southbound":
                self.southbound_count -= 1

class Bridge:
    def __init__(self):
        self.mutex = threading.Lock()
        self.direction_semaphore = DirectionSemaphore()
        self.crossed = 0

    def cross(self, direction):
        with self.mutex:
            if not self.direction_semaphore.wait(direction):
                print(f"{direction} vehicle is waiting to cross the bridge.")
                return

            self.crossed += 1
            car_number = self.crossed

            print(f"{direction} {car_number}. araç köprüyü geçiyor.")
            time.sleep(2)  # Simulating the time it takes to cross the bridge
            print(f"{direction} {car_number}. araç köprüyü geçti.")

            self.direction_semaphore.signal(direction)

class BridgeSimulation:
    def __init__(self, bridge):
        self.bridge = bridge

    def simulate_traffic(self):
        directions = ["Northbound", "Southbound"]

        def vehicle_thread(direction):
            for _ in range(3):  # Simulating 3 vehicles for each direction
                self.bridge.cross(direction)
                time.sleep(1)  # Time between consecutive vehicles

        threads = []
        for direction in directions:
            thread = threading.Thread(target=vehicle_thread, args=(direction,))
            thread.start()
            threads.append(thread)

        for thread in threads:
            thread.join()

if __name__ == "__main__":
    bridge = Bridge()
    simulation = BridgeSimulation(bridge)
    simulation.simulate_traffic()
