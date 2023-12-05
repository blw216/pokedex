import argparse
import csv
import typing

class MonsterDatabase:
    def __init__(self, database: typing.TextIO) -> None:
        # Possible monster types
        self.monster_types = set(["Ground", "Rock", "Water", "Electric", "Fire", "Flying", "Ice", "Psychic", "Bug", "Poison"])
        # Dictionary to hold monster data
        self.monster_database = {}
        # Read the CSV data into a dictionary
        with open(database, 'r') as f:
            reader = csv.DictReader(f)
            # Sort field names, this handles the case when the 
            # input CSV's can have different column order
            sorted_field_names = sorted(reader.fieldnames)
            sorted_rows = []
            for row in reader:
                sorted_row = {key: row[key] for key in sorted_field_names}
                sorted_rows.append(sorted_row)
            # Standardize monster name to lowercase for lookup
            # Add monster data to monster database dict
            for row in sorted_rows:
                monster_name = row['Name'].lower()
                self.monster_database[monster_name] = row
            # Close the input CSV file
            f.close()
        # Do some formatting of CSV values to make lookup easier later
        self.id_name_lookup = {}
        for monster in self.monster_database.keys():
            self.monster_database[monster]['Evolution_List'] = self.monster_database[monster]['Evolution'].split(',')
            self.monster_database[monster]['Weakness_List'] = self.monster_database[monster]['Weaknesses'].split(',')
            self.monster_database[monster]['Type_List'] = self.monster_database[monster]['Types'].split(',')
            self.id_name_lookup[self.monster_database[monster]['ID']] = self.monster_database[monster]['Name']
        # Build a data structure dict(str: list) for generating
        # Evolution paths later
        self.evolution_options = {}
        for v in self.monster_database.values():
            # remove nulls to make sure lists are properly empty, not ['']
            self.evolution_options[v['ID']] = [v for v in v['Evolution_List'] if v != '']

    def _get_monster_evolution(self, monster_id):
        # Get the evolution path data
        evolution_data = self.evolution_options
        # recursive case; If the monster has an evolution path
        if monster_id in evolution_data and evolution_data[monster_id]:
            evol_options = evolution_data[monster_id]
            # List to hold the evolution pathways
            evolution_pathways = []
            # For each monster ID in the list of possible options
            for i_monster_id in evol_options:
                # Recursively call the function to build evolution pathways
                evolution_pathways.extend(self._get_monster_evolution(i_monster_id))
            # Return the input monster id, and the output paths as a [[]]
            id_paths = [[monster_id] + path for path in evolution_pathways]
            return id_paths
        # base case; monster has no further (or none at all) evolution path
        else:
            return [[monster_id]]
    
    def monsterLookup(self, monster: str) -> str:
        # Make sure the monster name is lower case
        monster = monster.lower()
        # Get monster information
        # monster_name = self.monster_database[monster]['Name']
        monster_id = self.monster_database[monster]['ID']
        monster_types = self.monster_database[monster]['Type_List']
        monster_weaknesses = self.monster_database[monster]['Weakness_List']
        weak_against = []
        strong_against = []
        for key, val in self.monster_database.items():
            # Exclude the input monster
            if key != monster:
                i_monster_types = val['Type_List']
                # Get set intersection of the input monster's weaknesses
                # and every other monster in the database
                weakness_overlap = set(monster_weaknesses) & set(i_monster_types)
                # If the input monster is weak against a given monster,
                # Add it to the list
                if len(list(weakness_overlap)) > 0:
                    weak_against.append(val['Name'])
                # Do the same for the inverse, check if a given
                # monster is weak against the input monster
                i_monster_weakness = val['Weakness_List']
                strength_overlap = set(i_monster_weakness) & set(monster_types)
                # If so, add it to the list
                if len(list(strength_overlap)) > 0:
                    strong_against.append(val['Name'])
        # Add some conditional handling to create the required
        # output string for Codility
        if len(strong_against) > 0:
            pass
        else:
            strong_against = ["None"]
        if len(weak_against) > 0:
            pass
        else:
            weak_against = ["None"]
        # This is...not ideal string formatting technique, but
        # It'll do
        strong_against = "\n".join(['    ' + x for x in strong_against])
        weak_against = "\n".join(['    ' + x for x in weak_against])
        evol_paths = self._get_monster_evolution(monster_id)
        name_paths = [[self.id_name_lookup[id_] for id_ in ids] for ids in evol_paths]
        name_paths = [[" --> ".join(names)] for names in name_paths]
        name_paths = "\n    ".join([x[0] for x in name_paths])
        output = f"""ID:\n    {monster_id}
Strong Against:\n{strong_against}
Weak against:\n{weak_against}
Evolution:\n    {name_paths}
"""
        print(output) 

def main():
    parser = argparse.ArgumentParser(description='Print a Monster registry report.')
    parser.add_argument('database')
    parser.add_argument('monster')
    args = parser.parse_args()
    database = args.database
    monster = args.monster
    MonsterDatabase(database).monsterLookup(monster)

if __name__ == '__main__':
    main()