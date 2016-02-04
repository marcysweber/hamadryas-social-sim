
import constants
import copy

class FemaleState:
    underage, cycling, pregnant, nursing0, nursing1 = range(5)

class AgentClass:
    """
    defines an agent (in this case, a baboon) in the Simulation
    """
    #these values are defined in class seedgenerator.
    age = 0
    sex = ""
    femaleState = None
    maleState = None
    parents = []
    children = set()
    index = 0
    clanID = ""
    bandID = ""

    isleader = False

    def __init__(self, age, sex, femaleState,
        index, clanID, bandID, parents, children=None):
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

        #make sure sisters, aggressive, friends are empty lists not
        #null references

        if self.children == None:
            self.children = set()

        #make sure that children is a set
        #assert(type(self.children) is set)

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

    def update_indices(self, top_index):
        """
        increments all indices by top_index, to
        keep a unique index for an individual across
        a population
        """
        self.index += top_index
        if self.parents:
            self.parents += top_index

        children_list = list(self.children)
        for i in range(len(children_list)):
            children_list[i] += top_index
        self.children = set(children_list)

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














