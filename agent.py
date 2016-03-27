
import constants


class FemaleState:
    underage, cycling, pregnant, nursing0, nursing1 = range(5)

class MaleState:
    juvsol, sol, fol, lea = range(4)

class CompAbility:
    type1, type2, type3, type4 = range(4)

class AgentClass:
    """
    defines an agent (in this case, a baboon) in the Simulation
    """
    #these values are defined in class seedgenerator.
    age = 0
    sex = ""

    femaleState = None
    last_birth = 0

    maleState = None
    females = []
    malefols = []
    lottery = []
    compability = None

    parents = []
    children = set()

    index = 0
    clanID = ""
    bandID = ""
    OMU = ""

    dispersed = False


    def __init__(self, age, sex, femaleState, maleState,
        index, clanID, bandID, parents, OMUID, compability, females = [],
                 malefol = [], children = set(), last_birth = 0, lottery = [], dispersed = False
                 ):
        """
        constructor
        -----------
        parameters
        ----------
        number - the identification number of the individual in the population
        sex - sex of the individual as defined in constants.py
        age - age of individual in years

        relationship-related parameters
        -------------------------------
        parent - ID numbers of the individual's parents
        index - the index of this agent
        children - list of indices of this agent's children
        """
        #make sure age class and sex are valid
        sex = sex.lower()
        assert (constants.SEX_DICT.has_key(sex))

        self.age = float(age)
        self.sex = sex
        #self.is_alpha = is_alpha
        self.parents = parents
        self.index = index
        self.children = children
        self.clanID = clanID
        self.bandID = bandID
        self.femaleState = femaleState
        self.last_birth = last_birth
        self.maleState = maleState
        self.females = females
        self.setMaleFol(malefol)
        self.setOMUID(OMUID)
        self.lottery = lottery
        self.compability = compability
        self.dispersed = dispersed

        #make sure sisters, aggressive, friends are empty lists not
        #null references

        if self.children == None:
            self.children = set()

        #make sure that children is a set
        #assert(type(self.children) is set)

    def setOMUID(self, OMUID):
        print str(self.index) + "'s OMU ID is now " + str(OMUID)
        self.OMU = OMUID

    def getOMUID(self):
        return self.OMU

    def setMaleFol(self, malefol):
        print str(self.index) + "'s malefols are now " + str(malefol)
        self.malefols = malefol

    def getMaleFol(self):
        return self.malefols

    def get_selfstring(self):
        """
        returns the name of the agent in dot syntax
        """
        selfstring = ""

        if (self.sex == "m"):
            selfstring = str(self.index)

        else:
            selfstring = str(self.index) + " [shape=box]"

        selfstring += "[label=" + str(self.age) + "]"

        return selfstring

    def update_index(self, top_index):
        """
        increments all indices by top_index, to
        keep a unique index for an individual across
        a population
        """
        self.index += top_index
        self.clanID += top_index
        self.bandID += top_index

        if self.maleState == MaleState.lea:
            for i in range(0, len(self.females)):
                self.females[i] += top_index

            malefol = self.getMaleFol()
            for i in range(0, len(malefol)):
                malefol[i] += top_index

            self.setMaleFol(malefol)

            unique_male_fols = list(set(self.getMaleFol()))
            assert (self.getMaleFol() == unique_male_fols)
            assert self.index not in self.getMaleFol()

        if self.getOMUID() != "":
            self.setOMUID(self.getOMUID() + top_index)

        #this is correct

    def move_agent_to_group(self, destination):
        self.bandID = destination

    def get_dot_string(self, parent_group):
        """
        returns a string with the agent in dot syntax
        """
        outputstring = ""

        outputstring += self.get_selfstring() + ";\n"

        for child_index in self.children:
            if (child_index in parent_group.whole_set):
                outputstring += str(self.index) + " -> " +\
                 str(child_index) + "[color=red];\n"


        return outputstring

    def get_json_name(self):
        """
        returns the name of this object in JSON. This
        is used for visualizing populations in javascript
        """
        name_dict = {"name":self.index,
         "age":self.age, "sex":self.sex}

        return name_dict

    def get_json_links(self, parent_group):
        """
        returns links relating to this object in JSON.
        Used for visualizing populations in javascript
        """
        output = []

        for child_index in self.children:
            output_dict = {"source":self.index,
            "target":child_index, "type":"parent-child"}
            output.append(output_dict)

        return output

    def __str__(self):
        """
        returns human readable class description
        """
        output_string = "age:" + str(self.age) +\
            " sex:" + self.sex + " index: " +\
            str(self.index)

        return output_string














