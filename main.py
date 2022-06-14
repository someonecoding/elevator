class Building:
    floors = {}

    def __init__(self, floors):
        for i in range(1, floors + 1):
            self.floors[i] = Floor(self, i)

    def __getitem__(self, floor):
        return self.floors[floor]

    @property
    def max_floor(self):
        return list(self.floors.keys())[-1]

    @property
    def min_floor(self):
        return list(self.floors.keys())[0]


class Floor:

    def __init__(self, Building_Instance, floor):
        self.Building = Building_Instance
        self.floor = floor
        self.passengers = []

    @property
    def floor_directions(self):
        return [x.direction for x in self.passengers]

    @property
    def floor_destinations(self):
        return [x.DestinationFloor.floor for x in self.passengers]

    @property
    def frequent_direction(self):
        directions = self.floor_directions
        if directions.count('UP') == directions.count('DOWN'):
            return None
        else:
            return max(set(directions), key=directions.count)


class Passenger:

    class DestinationError(Exception):
        def __init__(self, message):
            self.message = message
            super().__init__(self.message)

        def __str__(self):
            return f'[!] {self.message}'

    def __init__(self, Floor_Instance, Destination_Floor_Instance):
        self.Floor = Floor_Instance
        self.Floor.passengers.append(self)

        if Destination_Floor_Instance.floor == self.Floor.floor:
            raise self.DestinationError("Destination is same as a floor.")
        elif (
            Destination_Floor_Instance.floor < self.Floor.Building.min_floor
            or
            Destination_Floor_Instance.floor > self.Floor.Building.max_floor
        ):
            raise self.DestinationError("Destination is out of bound.")
        else:
            self.DestinationFloor = Destination_Floor_Instance

    @property
    def direction(self):
        if self.DestinationFloor.floor < self.Floor.floor:
            return 'DOWN'
        else:
            return 'UP'


class Elevator:
    direction_bool = True
    capacity = 5
    destination = None

    def __init__(self, Building_Instance):
        self.Building = Building_Instance
        self.Floor = Building_Instance[Building_Instance.min_floor]
        self.passengers = []

    @property
    def passengers_queue(self):
        return sum([len(i.passengers) for i in self.Building.floors.values()])

    @property
    def space_left(self):
        return self.capacity - len(self.passengers)

    @property
    def direction(self):
        if self.direction_bool:
            return 'UP'
        else:
            return 'DOWN'

    def render(self):
        print('\n')
        for floor in list(self.Building.floors.values())[::-1]:
            flag = ">" if floor == self.Floor else " "
            print(f'{flag}floor: {floor.floor} p: {floor.floor_destinations}')

    def toggle_direction(self):
        self.direction_bool = not self.direction_bool

    def move(self):
        if self.direction_bool:
            self.Floor = self.Floor.Building[self.Floor.floor + 1]
        else:
            self.Floor = self.Floor.Building[self.Floor.floor - 1]

    def set_destination(self):
        if self.direction_bool:
            self.destination = max(
                [x.DestinationFloor for x in self.passengers],
                key=lambda item: item.floor,
                default=None
            )
        else:
            self.destination = min(
                [x.DestinationFloor for x in self.passengers],
                key=lambda item: item.floor,
                default=None
            )

    def passengers_load(self):
        while (
            self.space_left > 0
            and
            self.direction in [x.direction for x in self.Floor.passengers]
        ):
            for i in range(len(self.Floor.passengers)):
                if self.Floor.passengers[i].direction == self.direction:
                    self.passengers.append(self.Floor.passengers.pop(i))
                    print('Append!')
                    break

    def passengers_out(self):
        while self.Floor in [x.DestinationFloor for x in self.passengers]:
            for i in range(len(self.passengers)):
                if self.passengers[i].DestinationFloor == self.Floor:
                    del self.passengers[i]
                    print('Leaved!')
                    break

    def set_boundary_call(self):
        longest_up, longest_down = None, None

        for floor in self.Building.floors.values():
            direction_chocices = set(floor.floor_directions)

            if 'UP' in direction_chocices:
                if longest_up:
                    if floor.floor < longest_up:
                        longest_up = floor.floor
                else:
                    longest_up = floor.floor

            if 'DOWN' in direction_chocices:
                if longest_down:
                    if floor.floor > longest_down:
                        longest_down = floor.floor
                else:
                    longest_down = floor.floor

        if longest_down is None:
            self.destination = self.Building[longest_up]
        elif longest_up is None:
            self.destination = self.Building[longest_down]
        else:
            if (
                abs(self.Floor.floor - longest_up)
                <
                abs(self.Floor.floor - longest_down)
            ):
                self.destination = self.Building[longest_up]
            else:
                self.destination = self.Building[longest_down]

        self.direction_bool = self.Floor.floor < self.destination.floor

    def run(self):
        self.render()
        while self.passengers_queue > 0:

            destination_dummy = (
                self.Building[self.Building.max_floor]
                if self.direction_bool
                else self.Building[self.Building.min_floor]
            )

            if self.Floor.passengers:
                while self.Floor != (
                    self.destination or destination_dummy
                ):
                    self.passengers_out()
                    self.passengers_load()
                    self.set_destination()
                    self.move()
                    self.render()

                self.passengers_out()
                self.destination = None
                if self.Floor.frequent_direction is None:
                    pass
                else:
                    if self.Floor.frequent_direction != self.direction:
                        self.toggle_direction()

                continue
            else:
                self.set_boundary_call()
                while self.Floor != self.destination:
                    self.move()
                    self.render()


if __name__ == "__main__":
    a = Building(6)
    e = Elevator(a)
    Passenger(a[2], a[3])
    Passenger(a[4], a[3])
    Passenger(a[6], a[4])
    Passenger(a[6], a[4])
    Passenger(a[6], a[4])
    Passenger(a[6], a[4])
    Passenger(a[6], a[4])
    Passenger(a[6], a[4])

    e.run()
