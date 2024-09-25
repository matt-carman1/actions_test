"""
TEST DESCRIPTION: Checks the basic settings for the PRESETS toolbar options.
"""
import selenium 

# Import Squish wrappers
source(findFile("scripts", "maestro/maestro_handling.py"))
source(findFile('scripts', 'general/general.py'))
source(findFile("scripts", "maestro/project_table.py"))


def main():
    # Start maestro
    maestro = start_maestro()
    pt = ProjectTable()

  


