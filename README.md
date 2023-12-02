# pokedex
Python implementation of a Pokédex. Use the CLI to retrieve information about your favorite Pokemon.

data.csv:

```
ID,Name,Types,Weaknesses,Evolution
004,Banub,Fire,"Ground,Rock,Water",005
005,Banubeleon,Fire,"Ground,Rock,Water",006
006,Banubizard,"Fire,Flying","Rock,Electric,Water",
043,Octopeat,"Grass,Poison","Fire,Flying,Ice,Psychic",044
044,Octoplat,"Grass,Poison","Fire,Flying,Ice,Psychic","045,182"
045,Octonyte,"Grass,Poison","Fire,Flying,Ice,Psychic",
182,Bibyss,Grass,"Bug,Fire,Flying,Ice,Poison",
```

Examples:

```
$ python pokedex.py  ./data.csv Banub

ID:
    004
Strong Against:
    Octopeat
    Octoplat
    Octonyte
    Bibyss
Weak against:
    None
Evolution:
    Banub --> Banubeleon --> Banubizard

---------------------------------------

python pokedex.py  ./data.csv octopeat

ID:
    043
Strong Against:
    Bibyss
Weak against:
    Banub
    Banubeleon
    Banubizard
Evolution:
    Octopeat --> Octoplat --> Octonyte
    Octopeat --> Octoplat --> Bibyss
```
