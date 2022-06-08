from random import randint, choices
from itertools import chain



class Elevator:
    #generation and inheritance variables
    min_floor_gen = 5
    max_floor_gen = 10
    pass_per_floor_gen = 10
    capacity = 5

    __current_floor = 1
    __current_passengers = []
    __floors_schema = None
    __directions = {
        0: 'DOWN',
        1: 'UP'
    }
    __current_direction = __directions[1]
    __elevator_destination = None


    @property
    def floors_queue_len(self):
        return len(list(chain(*self.__floors_schema.values())))


    @property
    def space_left(self):
        return self.capacity - len(self.__current_passengers)


    @property
    def floor_passengers(self):
        return self.__floors_schema[self.__current_floor]


    @property
    def floor_passengers_directions(self):
        return [x[1] for x in self.__floors_schema[self.__current_floor]]

    
    @property
    def current_passengers_destinations(self):
        return [x[0] for x in self.__current_passengers]



    #sets random floor height based on min and max floor generator values
    def __init__(self, passengers_autogen=False):
        self.floors = randint(self.min_floor_gen, self.max_floor_gen)
        self.__floors_schema = self.gen_floors_schema(autogen=passengers_autogen)


    #generates floors schema with fake passengers data if autogen = True
    def gen_floors_schema(self, autogen):
        data = {}

        if not autogen:
            pass_per_floor = 0
        else:
            pass_per_floor = self.pass_per_floor_gen

        for i in range(1, self.floors + 1):
            passenger_floor_choices = list(range(1, self.floors + 1))
            passenger_floor_choices.remove(i)
            passengers = []

            for _ in range(randint(0, pass_per_floor)):
                passenger_floor_choice = choices(passenger_floor_choices)[0]
                passengers.append(
                    (
                        passenger_floor_choice,
                        self.__directions[int(i < passenger_floor_choice)]
                    )
                )

            data[i] = passengers
        
        return data


    #move based on direction
    def move(self):
        if self.__current_direction == 'UP':
            self.__current_floor += 1
        else:
            self.__current_floor -= 1
        self.render()



    def set_elevator_destination(self):
        if self.__current_direction == 'UP':
            self.__elevator_destination = max(self.current_passengers_destinations, default=self.__elevator_destination)
        else:
            self.__elevator_destination = min(self.current_passengers_destinations, default=self.__elevator_destination)

    

    #finds best floor choice for next iteration when current floor is empty
    def find_boundary_floor(self):
        step = 1 if self.__current_direction == 'UP' else -1
        for i in list(range(1, self.floors+1))[::step]:
            for j in self.__floors_schema[i]:
                if j[1] == self.__current_direction:
                    return i
                else:
                    self.toggle_direction()
                    return self.find_boundary_floor()
        
    

    def toggle_direction(self):
        toggle_to = list(self.__directions.values())
        toggle_to.remove(self.__current_direction)
        self.__current_direction = toggle_to[0]
        return self.__current_direction
        

    #removes passengers from schema and append in current passengers
    #checks if enough space and directions are equals
    #log on enter
    def passengers_load(self):
        if self.floor_passengers != []:
            while self.space_left > 0 and self.__current_direction in self.floor_passengers_directions:
                for i in range(len(self.floor_passengers)):
                    if self.floor_passengers[i][1] == self.__current_direction:
                        print(f"{self.floor_passengers[i]} entered!")
                        self.__current_passengers.append(
                            self.__floors_schema[self.__current_floor].pop(i)
                        )
                        break



    #removes all current passengers if floors are equals
    #log on leave
    def passengers_out(self):
        while self.__current_floor in self.current_passengers_destinations:
            for i in range(len(self.__current_passengers)):
                if self.__current_passengers[i][0] == self.__current_floor:
                    print(f"{self.__current_passengers[i]} leaved!")
                    del self.__current_passengers[i]
                    break

    
    #renders elevator state
    def render(self):
        print("\n")
        for key in list(self.__floors_schema.keys())[::-1]:
            e_floor = ">" if key == self.__current_floor else " "
            print(f"{e_floor} floor: {key} p: {self.__floors_schema[key]}")

                
    
    def run(self):

        #renders initial state
        self.render()
        self.__current_floor = self.find_boundary_floor()
        if self.__current_floor != 1:
            self.render()

        #loops while no passengers left
        while self.floors_queue_len != 0:

            #loops while reaches destination
            destination_dummy = self.floors if self.__current_direction == 'UP' else 1
            while self.__current_floor != (self.__elevator_destination or destination_dummy):
                self.passengers_out()
                
                if self.__current_floor != self.__elevator_destination:
                    self.passengers_load()
                    self.set_elevator_destination()
                
                self.move()
            
            self.passengers_out()
            self.__elevator_destination = None

            #destination floor not empty scenario
            if self.floor_passengers != []:
                directions = [x[1] for x in self.floor_passengers]
                #if UP and DOWN passengers directions are equals leave same elevator direction
                if directions.count('UP') == directions.count('DOWN'):
                    pass
                #counts most frequent direction choice, then compares to current elevator direction
                #if not equal -> toggle, else leaves same value
                elif self.__current_direction != max(set(directions), key = directions.count):
                    self.toggle_direction()
                continue
            #destination floor empty scenario
            else:
                self.__current_floor = self.find_boundary_floor()
                self.render()
                continue

            

            


if __name__ == "__main__":
    a = Elevator(passengers_autogen=True)
    a.run()
    
