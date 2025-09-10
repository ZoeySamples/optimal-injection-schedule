class InjectionSimulator(object):
    """InjectionSimulator class runs the simulation of medication usage.
    
    Methods:
        __init__(self, total_people, namelist, dose_info, num_vials,
                vial_volume)
        check_legal_dosages()
        do_injections(dose)
        update_vials_used()
        run_simulation()
    """

    def __init__(self, total_people, namelist, dose_info, num_vials=20,
                 vial_volume=5.0):
        """InjectionSimulator Class Constructor to initialize the object and
        determine the actual dosages instead of unit doses.
        
        Input Arguments:
        total_people (int): The number of people doing injections.
        namelist (list of strings): The names of everyone in the simulation.
        dose_info (array): The trial's permutation of each person's dosage.
        num_vials (int): The number of medication vials to simulate
        vial_volume (float): The volume of each medication vial.
        """
        
        self.total_people = total_people
        self.num_vials = num_vials
        self.vial_volume = vial_volume

        # Convert the dose information into actual dosages and store in a list.
        self.dosage_dicts = []
        for i in range(total_people):
            info = {
                "dosage": round(dose_info[0 + 2*i]*dose_info[1 + 2*i], 2),
                "frequency": dose_info[1 + 2*i],
                "name": namelist[i]
                }
            self.dosage_dicts.append(info)

        # Sort dosage_dicts by largest to smallest dosage for compatibility.
        self.dosage_dicts = sorted(self.dosage_dicts,
                                   key=lambda x: x["dosage"], reverse=True)
          
        # Initialize simulation status variables.
        self.injections_handled = [False]*self.total_people
        self.leftover_vial = False
        self.leftover_amount = 0.0
        self.vials_used = 0
        self.waste = 0.0
        self.left_in_vial = vial_volume
        self.check_legal_dosages()

    def check_legal_dosages(self):
        """This method tests edge cases and terminates the simulation if there
        is an invalid condition.
        """
        # Make sure the largest dosage is not too large.
        self.early_termination = False
        if self.dosage_dicts[0]["dosage"] > self.vial_volume:
            self.early_termination = True

        # Make sure there is not a negative dose.
        if self.dosage_dicts[-1]["dosage"] <= 0:
            self.early_termination = True
    
    def do_injection(self, dose):
        """This method determines if there is enough medication left in the
        vial to do the injection, then does the injection.

        Input arguments:
        dose (float): the dose of the current person's injection.

        Returns:
        True: if injection was a success.
        False: if there is not enough medication to do the injection.        
        """

        # Check the leftover vial first if there is one.
        if self.leftover_vial and (self.leftover_amount - dose >= 0):
            self.leftover_amount = self.leftover_amount - dose
            if (self.leftover_amount - self.dosage_dicts[-1]["dosage"] < 0):
                self.waste = self.waste + self.leftover_amount
                self.leftover_vial = False
            return True
        elif (self.left_in_vial - dose) >= 0:
            self.left_in_vial = self.left_in_vial - dose
            return True
        else:
            return False
                
    def update_vials_used(self):
        """This method updates the number of vials used."""

        # Discard vial if there isn't enough for anyone, then start a new one.
        if self.left_in_vial < self.dosage_dicts[-1]["dosage"]:
            self.waste = self.waste + self.left_in_vial
            self.vials_used = self.vials_used + 1
            self.left_in_vial = self.vial_volume

        # Create leftover vial if there is enough for some but not all people.    
        elif (self.left_in_vial >= self.dosage_dicts[-1]["dosage"]
              and self.left_in_vial < self.dosage_dicts[0]["dosage"]):
            self.leftover_vial = True
            self.leftover_amount = self.left_in_vial
            self.vials_used = self.vials_used + 1
            self.left_in_vial = self.vial_volume
                
    def run_simulation(self):
        """This method runs the simulation.
        
        Returns a list with the following information:
        waste (float): The amount of wasted medication.
        day (int): How many days it took to use the allocated number of vials.
        dosage_dicts (list of dicts): The dosage info and name of each person.
        """
        if self.early_termination:
            return None
        self.day = 1
        while self.vials_used < self.num_vials:
            self.injections_handled = [False]*self.total_people
            while False in self.injections_handled:
                for i in range(self.total_people):
                    # If someone is due for an injection today, and they
                    # haven't done it yet, then do the injection.
                    if (self.day % self.dosage_dicts[i]["frequency"] == 0 and
                        self.injections_handled[i] == False):
                        self.injections_handled[i] = self.do_injection(
                            dose = self.dosage_dicts[i]["dosage"])
                    else:
                        # If they aren't due for an injection today, then
                        # treat their injection as handled for today.
                        self.injections_handled[i] = True
                self.update_vials_used()
            self.day = self.day + 1
            
        return [self.waste, self.day, self.dosage_dicts]