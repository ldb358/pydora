from random import randint;
from math import floor;
gamelist = ["Dota 2", "Hon", "Diablo 3", "Starcraft 2"];
totals  = [0,0,0,0]

for i in range(0, 10000, 1):
    game = randint(0,3);
    totals[game] += 1 ;
max = 0;
for x in range(0, 4, 1):
    if(totals[x] > totals[max]):
        max = x;
        
print gamelist[max], "Won with", totals[max]/100, "Percent", totals[max]