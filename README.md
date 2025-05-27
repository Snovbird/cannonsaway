# Cannon's away level maker
Level maker for pvz2 and pvz2 reflourished Cannon's away minigame
Works with python 3.10+

**NEEDS WXPYTHON**

If not installed on your device yet: `pip install wxpython`

# How to use (it's really simple!):

1) Download the cannonsawaymaker.pyw file and put it in any empty folder
2) In this same folder, download the `rawlvl` folder, the json inside will serve as reference for new lvls made
3) Double click on `cannonsawaymaker.pyw`
4) A panel with a list of zombies will appear, only the rows from top to bottom matter. I also made custom flying pathways, but you can change them in `rawlvl.json` if you made them using this [tool](https://docs.google.com/spreadsheets/d/1MkUcyy6HAlTxln-cP0ZisAU5r02ZPSqhVEsSjP3NvGM/copy) (I will probably integrate this in the interface later on)
5) Click on the colored 'toggle' button to switch to grid items (currently gravestones-coconut-banana-puffapple, and then goes back to zombies)
6) The 'NextWave' button is what creates a new lvl file. Just click it after you are done with the current wave to add more zombies for your next wave. Always press this button to save your work


# Other comments:

* You can edit `rawlvl.json` and remove the **IPP_protect** and **rails** modules to get rid of the magnifying grass on rails
* You can add the **IPP** to the modules list to have the classic coconut cannons in place