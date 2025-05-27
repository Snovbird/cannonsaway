import wx
import json
import os

zombies = ["pirate_captain_parrot","parrotrousle_parrot",'seagull','pelican','skycity_battleplane','skycity','skycity_armor(1)','skycity_armor(2)','skycity_armor(4)','skycity_flag','skycity_flag_veteran','skycity_rocket']
labelcolors = {"pirate_captain_parrot":"#C70000","parrotrousle_parrot":"#00C753",'seagull':"#C2D300",'pelican':"#FF7300",'skycity_battleplane':"#9E9E9E",'skycity_flag':"#c30202",'skycity_flag_veteran':wx.NullColour,'skycity_armor(4)':wx.NullColour,'skycity_rocket':"#00C7C4",'skycity_armor(2)':wx.NullColour,'skycity_armor(1)':wx.NullColour,'skycity':wx.NullColour}

class GridApp(wx.Frame):
    def __init__(self):
        super().__init__(None, title="Cannon's away level maker", size=(126*len(zombies), 600))
        print()
        # Main panel
        self.panel = wx.Panel(self)
        
        # init variables
        self.filecount = 1
        self.entity_data_list = []
        self.gridspawns = []
        self.gridpos = []
        self.buttons = []
        self.wavecount = 0
        self.showing_what = "zombies"
        self.script_directory = os.path.dirname(os.path.abspath(__file__))
        with open(os.path.join(self.script_directory,'rawlvl',"rawlvl.json")) as file:
            self.basejson = json.load(file)


        # Create the grid of buttons
        self.create_grid()
        
        # Create status bar
        self.status_bar = self.CreateStatusBar()
        self.status_bar.SetStatusText("Current Wave: " + f"{self.wavecount+1} ")
        # Center the window
        self.Centre()
        
    def create_grid(self):
        # Create a grid sizer (5 rows, 6 columns)
        grid_sizer = wx.GridSizer(rows=6, cols=len(zombies), vgap=5, hgap=5)
        
        # Add buttons 1-25 followed by the 5 special function buttons
        for row in range(5):  # 6 rows
            for col, entity_type in enumerate(zombies):  # depending on how many zombies
                # Calculate the position in the grid (0-29)
                position = row * 6 + col
                
                if position < 6*len(zombies):
                    # Numbered buttons (1-25)
                    btn = wx.Button(self.panel, label=f"{entity_type}{row}")
                    btn.Bind(wx.EVT_BUTTON, self.on_numbered_button)
                    grid_sizer.Add(btn, 1, wx.EXPAND)
                    self.buttons.append(btn)
                    btn.SetBackgroundColour(labelcolors[entity_type])
                else:
                    # Special function buttons
                    func_position = position - 6*len(zombies)  # 0-4
                    
        # Button 1: Clear list after confirmation
        browse_btn = wx.Button(self.panel, label="Browse Jsons")
        browse_btn.Bind(wx.EVT_BUTTON, self.on_browse_files)
        grid_sizer.Add(browse_btn, 1, wx.EXPAND)
        # Button 2: toggle 
        self.toggle_btn = wx.Button(self.panel, label="Toggle to\nGRAVESTONES")
        self.toggle_btn.SetBackgroundColour("#BBBBBB")
        self.toggle_btn.Bind(wx.EVT_BUTTON, self.on_toggle_buttons)
        grid_sizer.Add(self.toggle_btn, 1, wx.EXPAND)
        # Button 3:  list
        NextWave_btn = wx.Button(self.panel, label="NextWave")
        NextWave_btn.Bind(wx.EVT_BUTTON, self.on_nextwave)
        NextWave_btn.SetBackgroundColour("#FD0909")
        grid_sizer.Add(NextWave_btn, 1, wx.EXPAND)
        # Button 4: NextWave
        display_btn = wx.Button(self.panel, label="DISPLAY")
        display_btn.Bind(wx.EVT_BUTTON, self.on_display)
        grid_sizer.Add(display_btn, 1, wx.EXPAND)
        # Button 5: Exit
        initgi_btn = wx.Button(self.panel, label="GI\nInitial")
        initgi_btn.Bind(wx.EVT_BUTTON, self.on_chooseGI)
        grid_sizer.Add(initgi_btn, 1, wx.EXPAND)
        # Button 6: unused
        # exit_btn = wx.Button(self.panel, label="Choose\nFile")
        # exit_btn.Bind(wx.EVT_BUTTON, self.on_exit)
        # grid_sizer.Add(exit_btn, 1, wx.EXPAND)
        # Button 7: Exit
        exit_btn = wx.Button(self.panel, label="Exit")
        exit_btn.Bind(wx.EVT_BUTTON, self.on_exit)
        grid_sizer.Add(exit_btn, 1, wx.EXPAND)

        # Set the sizer for the panel
        self.panel.SetSizer(grid_sizer)
    
    def on_browse_files(self, event):
        dlg = wx.FileDialog(self, "Choose a file", wildcard="*.json", style=wx.FD_OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            # wx.MessageBox(f"Selected file: {path}", "File Selected")
            self.status_bar.SetStatusText("Current Wave: " + f"{self.wavecount+1}\t-->" + f"Selected file: {os.path.basename(path)}")
            self.entity_data_list = []
            self.gridspawns = []
            self.gridpos = []
            
            with open(path) as newjson:
                self.basejson = json.load(newjson)

            currentindexnumber = -1
            try:
                while self.basejson['objects'][currentindexnumber]['aliases'][0][:4] != 'Wave':
                    currentindexnumber -= 1
                else:
                    self.wavecount = int(self.basejson['objects'][currentindexnumber]['aliases'][0][-1])
                    print("WAVECOUNT: ", self.wavecount)
            except Exception as e:
                wx.MessageBox("WaveCount error: " + str(e),"Error")
                
    def on_numbered_button(self, event):
        # Get the button entity_type
        btn = event.GetEventObject()
        entity_type = btn.GetLabel()
        if entity_type:
            if self.showing_what == "zombies":
                # Create a dictionary and append to the list
                data = {"Row": int(entity_type.replace('(','').replace(')','')[-1]), "Type": f"RTID({entity_type.replace('(','').replace(')','')[:-1]}@ZombieTypes)"}
                self.entity_data_list.append(data)
            else:
                spec_entity = entity_type.replace('(','').replace(')','')[:-2].replace("GRAVE",'gravestone_pirate@GridItemTypes')
                data = {"Count": 1, "Type": f"RTID({spec_entity})"}
                lawnpos = {"mX": int(entity_type.replace('(','').replace(')','')[-1]), "mY": int(entity_type.replace('(','').replace(')','')[-2])}
                self.gridpos.append(lawnpos)
                self.gridspawns.append(data)
            # Update the status bar
            self.status_bar.SetStatusText("Current Wave: " + f"{self.wavecount+1}\t-->" + f"Added: {data}")
    
    def on_clear_list(self, event): # UNUSED
        #  confirmation dialog
        dlg = wx.MessageDialog(
            self, 
            "Are you sure you want to clear the list?",
            "Confirmation",
            wx.YES_NO | wx.ICON_QUESTION
        )
        
        result = dlg.ShowModal()
        if result == wx.ID_YES:
            self.filecount = 1 # operations to clear:
            # reset every time
            self.entity_data_list = []
            self.gridspawns = []
            self.gridpos = []
            #
            self.buttons = []
            self.wavecount = 0
            self.showing_what = "zombies"
            with open(os.path.join(self.script_directory,'DONOTTOUCH',"rawlvl.json")) as file:
                self.basejson = json.load(file)
            self.status_bar.SetStatusText("Current Wave: " + f"{self.wavecount+1}\t-->" + "RESET COMPLETE")
        dlg.Destroy()
    
    def on_toggle_buttons(self,event):
        # Toggle between numbers and letters
        if self.showing_what == "zombies":
            self.status_bar.SetStatusText("Current Wave: " + f"{self.wavecount+1}\t-->" + "Switched to gravestones")

            self.showing_what = "gravestones"
            self.toggle_btn.SetLabel(f"toggle to\nCOCONUTGIFT")
            self.toggle_btn.SetBackgroundColour("#FFB55B")
            rowcount = -1
            for i, btn in enumerate(self.buttons):
                # columncount = (i % len(zombies)) + 9 - len(zombies) # for right to left
                columncount = i % len(zombies) # left to right
                
                if columncount == 0:
                    rowcount += 1
                if columncount > 4 and columncount <= 8:
                    btn.SetBackgroundColour("#09F5FD")
                    btn.SetLabel(f"")
                elif columncount > 8:
                    btn.SetBackgroundColour(wx.NullColour)
                    btn.SetLabel(f"")
                else:
                    btn.SetBackgroundColour("#BBBBBB")
                    btn.SetLabel(f"GRAVE{rowcount}{columncount}")
                

        elif self.showing_what == "gravestones":
            self.status_bar.SetStatusText("Current Wave: " + f"{self.wavecount+1}\t-->" + "Switched to coconut")

            self.showing_what = "coconut"
            self.toggle_btn.SetLabel(f"toggle to\nBANANAGIFT")
            self.toggle_btn.SetBackgroundColour("#FFDE59")
            rowcount = -1 
            for i, btn in enumerate(self.buttons):
                # columncount = (i % len(zombies)) + 9 - len(zombies) # for right to left
                columncount = i % len(zombies) # left to right

                if columncount == 0:
                    rowcount += 1
                if columncount > 4 and columncount <= 8:
                    btn.SetBackgroundColour("#09F5FD")
                    btn.SetLabel(f"")
                elif columncount > 8:
                    btn.SetBackgroundColour(wx.NullColour)
                    btn.SetLabel(f"")
                else:
                    btn.SetBackgroundColour("#FFB55B")
                    btn.SetLabel(f"SpawnCoconut@.{rowcount}{columncount}")


        elif self.showing_what == "coconut":
            self.status_bar.SetStatusText("Current Wave: " + f"{self.wavecount+1}\t-->" + "Switched to banana")

            self.showing_what = "banana"
            self.toggle_btn.SetLabel(f"toggle to\nPINEAPPLE")
            self.toggle_btn.SetBackgroundColour("#00FF15")
            rowcount = -1
            for i, btn in enumerate(self.buttons):
                # columncount = (i % len(zombies)) + 9 - len(zombies) # for right to left
                columncount = i % len(zombies) # left to right

                if columncount == 0:
                    rowcount += 1
                if columncount > 4 and columncount <= 8:
                    btn.SetBackgroundColour("#09F5FD")
                    btn.SetLabel(f"")
                elif columncount > 8:
                    btn.SetBackgroundColour(wx.NullColour)
                    btn.SetLabel(f"")
                else:
                    btn.SetBackgroundColour("#FFDE59")
                    btn.SetLabel(f"SpawnBanana@.{rowcount}{columncount}")
            
        elif self.showing_what == "banana":
            self.status_bar.SetStatusText("Current Wave: " + f"{self.wavecount+1}\t-->" + "Switched to PuffApple")

            self.showing_what = "pineapple"
            self.toggle_btn.SetLabel(f"toggle to\nZOMBIES")
            self.toggle_btn.SetBackgroundColour(wx.NullColour)
            rowcount = -1
            for i, btn in enumerate(self.buttons):
                # columncount = (i % len(zombies)) + 9 - len(zombies) # for right to left
                columncount = i % len(zombies) # left to right

                if columncount == 0:
                    rowcount += 1
                if columncount > 4 and columncount <= 8:
                    btn.SetBackgroundColour("#09F5FD")
                    btn.SetLabel(f"")
                elif columncount > 8:
                    btn.SetBackgroundColour(wx.NullColour)
                    btn.SetLabel(f"")
                else:
                    btn.SetBackgroundColour("#00FF15")
                    btn.SetLabel(f"SpawnPineapple@.{rowcount}{columncount}")
        else: # return to zombies
            self.showing_what = "zombies"
            self.toggle_btn.SetLabel(f"toggle to\nGRAVESTONES")
            self.toggle_btn.SetBackgroundColour("#BBBBBB")
            rowcount = -1
            
            for i, btn in enumerate(self.buttons):
                columncount = i % len(zombies) # left to right
                if columncount == 0:
                    rowcount += 1
                currententity = zombies[columncount]
                btn.SetLabel(currententity + f'{rowcount}')
                # btn.SetBackgroundColour(wx.NullColour)
                btn.SetBackgroundColour(labelcolors[currententity])
            self.status_bar.SetStatusText("Current Wave: " + f"{self.wavecount+1}\t-->" + "Switched to zombies")

    
    def on_nextwave(self,event):
        with open(os.path.join(self.script_directory,f"pirate{self.filecount}.json"), 'w') as output_file:
            json.dump(self.basejson, output_file, indent=4)
        if self.entity_data_list:
            self.script_directory = os.path.dirname(os.path.abspath(__file__))
            if self.wavecount == 0:
                while os.path.exists(os.path.join(self.script_directory,f"pirate{self.filecount}.json")):
                    self.filecount +=1
            
            self.wavecount +=1

            # Needs 'AddToZombiePool' attribute when it's wave 1
            if self.wavecount == 1 :
                self.basejson['objects'].append({ "aliases": [ "Wave1" ], "objclass": "SpawnZombiesJitteredWaveActionProps", "objdata": { "AddToZombiePool": [ { "Type": "RTID(seagull@ZombieTypes)" } ], "Zombies": self.entity_data_list } })
            else:
                format_entities = { "aliases": [ f"Wave{self.wavecount}" ], "objclass": "SpawnZombiesJitteredWaveActionProps", "objdata": { "Zombies": self.entity_data_list} }
                self.basejson['objects'].append(format_entities)

            # Checking if only zombies or if there are grid spawns event
            if self.gridspawns: # Grid spawns + zombies
                self.basejson['objects'][10]['objdata']['Waves'].append([f"RTID(Wave{self.wavecount}@CurrentLevel)",f"RTID(deletegrave@.)",f"RTID(GridSpawn{self.wavecount}@.)"])
                self.basejson['objects'].append({"aliases":[f"GridSpawn{self.wavecount}"], "objclass": "SpawnGravestonesWaveActionProps", "objdata": { "GravestonePool": self.gridspawns, "SpawnPositionsPool": self.gridpos, "SpawnEffectAnimID": "POPANIM_EFFECTS_PLANT_BURNT", "SpawnSoundID": "Play_Zomb_Egypt_TombRaiser_Grave_Rise", "DisplacePlants": True, "RandomPlacement": False, "ShakeScreen": True, "GridClassesToDestroy": [] }})                    
            else: # only zombies
                self.basejson['objects'][10]['objdata']['Waves'].append([f"RTID(Wave{self.wavecount}@CurrentLevel)"])
            
            self.basejson['objects'][10]['objdata']['WaveCount'] = len(self.basejson['objects'][10]['objdata']['Waves'])

            with open(os.path.join(self.script_directory,f"pirate{self.filecount}.json"), 'w') as output_file:
                json.dump(self.basejson, output_file, indent=4) #pretty formatting
            # important to reset
            self.entity_data_list = []
            self.gridspawns = []
            self.gridpos = []
            self.status_bar.SetStatusText("Current Wave: " + f"{self.wavecount+1}")
        else:
            wx.MessageBox("Needs at least 1 zombie in the wave", "Error", wx.OK | wx.ICON_ERROR)

    def on_display(self,event):
        # Create a new frame to display the list
        list_frame = ListFrame(self, self.entity_data_list,self.gridspawns)
        list_frame.Show()

    def on_chooseGI(self,event):
        class chooseGI(wx.Frame):
            def __init__(subself, parent):
                super().__init__(parent, title="Place Grid Items", size=(600, 450))
                subself.panel = wx.Panel(subself)
                subself.subcreate_grid()
                subself.Centre()
                subself.griddicts = []

            def subcreate_grid(subself):
                subgrid_sizer = wx.GridSizer(rows=6, cols=5, vgap=5, hgap=5)
                
                for row in range(5):  # 6 rows
                    for col in range(5): # 5 columns
                        subbtn = wx.Button(subself.panel, label=f"{row}{col}") # .replace("GRAVE",'gravestone_pirate@GridItemTypes')
                        subbtn.Bind(wx.EVT_BUTTON, subself.on_button)
                        if col == 0:
                            subbtn.SetBackgroundColour("#6D4B4B")
                        subgrid_sizer.Add(subbtn, 1, wx.EXPAND)
                # Save and quit
                subbtn = wx.Button(subself.panel, label=f"WRITE") # .replace("GRAVE",'gravestone_pirate@GridItemTypes')
                subbtn.Bind(wx.EVT_BUTTON, subself.on_saveinitgrid)
                subgrid_sizer.Add(subbtn, 1, wx.EXPAND)

                subself.panel.SetSizer(subgrid_sizer)

            def on_button(subself, subevent):
                subbtn = subevent.GetEventObject()
                subbtn.SetBackgroundColour("#4D4D4D")
                gipos = subbtn.GetLabel()
                dictofgi = { "GridX": int(gipos[-1]), "GridY": int(gipos[-2]), "Level": -1, "TypeName": "gravestone_pirate" }
                subself.griddicts.append(dictofgi)

            def on_saveinitgrid(subself,subevent):                    
                if subself.griddicts:
                    for grt in subself.griddicts:
                        self.basejson['objects'][4]['objdata']['InitialGridItemPlacements'].append(grt)
                    else:
                        pass
                subself.Close()

        # run the subclass
        chooseGI(self).Show()


    def on_exit(self,event):
        # Close the application
        if self.wavecount % 2 != 0:
            # print(self.entity_data_list,"\nLISTLENGTH IS",len(self.entity_data_list) % 2 != 0)
            wx.MessageBox("You need an even number of waves", "Error", wx.OK | wx.ICON_ERROR)
        else:
            self.Close()
    

                


class ListFrame(wx.Frame): # to display it
    def __init__(self, parent, data_list,grid_list):
        super().__init__(parent, title="List Contents", size=(400, 300))
        
        panel = wx.Panel(self)
        
        # Create a text control to display the list
        self.text_ctrl = wx.TextCtrl(
            panel,
            style=wx.TE_MULTILINE | wx.TE_READONLY | wx.HSCROLL
        )
        
        # Format and display the list contents
        content = ""
        for i, item in enumerate(data_list):
            content += f"Item {i+1}: {item}\n"
        content += "\n"
        if grid_list:
            for i, item in enumerate(grid_list):
                content += f"Griditem {i+1}: {item}\n"
        if not content:
            content = "List is empty"
            
        self.text_ctrl.SetValue(content)
        
        # Create a sizer
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.text_ctrl, 1, wx.ALL | wx.EXPAND, 10)
        
        # Add a close button
        close_btn = wx.Button(panel, label="Close")
        close_btn.Bind(wx.EVT_BUTTON, self.on_close)
        sizer.Add(close_btn, 0, wx.ALL | wx.CENTER, 10)
        
        panel.SetSizer(sizer)
        
        # Center the window relative to the parent
        self.Centre()
    
    def on_close(self,event):
        self.Close()



if __name__ == "__main__":
    app = wx.App()
    frame = GridApp()
    frame.Show()
    app.MainLoop()
