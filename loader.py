"""
Macaque Simulation Project
Adeesha Ekanayake 
5/12/2013

loader.py
---------
loads data from excel document into memory. The excel workbook must be
structured as follows:
    There must be 4 sheets in the book in the following order:
    1. Life table
    2. Dispersal table
    3. Friendship table
    4. Dominance table
"""

import xlrd
from lifetable import LifeTable
import dispersal
from dispersaltable import DispersalTable
from translocation_table import TranslocationTable

def load_data():
    """
    convenient method to quickly load data from excel file

    returns
    -------
    data from the excel sheet as described by class Loader
    """
    loader = Loader()
    loader.load_data()

    return loader

class Loader:
    """
    loads data from the excel document on the following areas:
        * Lifetable
        * Dispersal
        * Friendships
        * Dominance
    """

    life_table = None
    competitive_table = None

    EXCEL_FILENAME = "filoha_lifetable.xlsx"
    STARTING_ROW = 2 #the first 2 rows are headers, so reader must avoid them

    def test(self):
        """
        convenience class used for testing
        """
        #load the excel book
        book = xlrd.open_workbook(self.EXCEL_FILENAME)

        #load dispersaltable
        competitive_table_sheet = book.sheet_by_index(1)
        self.competitive_table = self.load_competitive_table(competitive_table_sheet)

        print self.competitive_table

    def load_data(self):
        """
        loads data from the excel file into memory

        returns
        -------
        dictionary with the following structure
            |- "life_table_dict" : LifeTable object
            |- CompetitiveTable object

        """

        #load the excel book
        book = xlrd.open_workbook(self.EXCEL_FILENAME)

        #load lifetable
        life_table_sheet = book.sheet_by_index(0)
        self.life_table = self.load_life_table(life_table_sheet)

        #load competitivetable
        competitive_table_sheet = book.sheet_by_index(1)
        self.competitive_table = self.load_competitive_table(competitive_table_sheet)

        """
        #load translocation table
        translocation_table_sheet = book.sheet_by_index(4)
        self.translocation_table =\
         self.load_translocation_table(translocation_table_sheet)
         """
    def load_life_table(self, life_table_sheet):
        """
        loads the life table into memory

        lifetable must be formatted as follows:
        -------------------------------------------------------
        |female	    | |male				      |
        -------------------------------------------------------
        |age| |qx|bx| |qx|bx|
        -------------------------------------------------------

        qx: chance of dying this TURN
        bx: chance of giving birth this year


        parameters
        ----------
        life_table_sheet: the sheet with the life table in it

        returns
        -------
        a LifeTable object
        """
        end_flag = True #used to let user customize number of rows in excel
                         #file by setting an END flag at the end of the table

        life_table = LifeTable()

        for row_index in range (self.STARTING_ROW, life_table_sheet.nrows):

            if life_table_sheet.cell_value(row_index,0) == 'END':
                end_flag = False

            if end_flag:
                #parameters for female
                age = life_table_sheet.cell_value(row_index,0)
                qx = life_table_sheet.cell_value(row_index,1)
                bx = life_table_sheet.cell_value(row_index,2)

                life_table.female_life_table[age] = (qx, bx)

                #parameters for male
                age = life_table_sheet.cell_value(row_index,0)
                qx = life_table_sheet.cell_value(row_index,4)
                bx = life_table_sheet.cell_value(row_index,5)

                life_table.male_life_table[age] = (qx, bx)

        return life_table

    def load_competitive_table(self, competitive_table_sheet):
        """
        loads dispersal table into memory.

        This table contains data on emigration and immigration for males
        by age class. Since females do not leave the group in our
        model, this table only concerns males.
        """
        end_flag = True #used to let user customize number of rows in excel
                         #file by setting an END flag at the end of the table

        competitive_table = dispersal.Competitive()

        for row_index in range (self.STARTING_ROW, competitive_table_sheet.nrows):

            if competitive_table_sheet.cell_value(row_index,0) == 'END':
                end_flag = False

            elif end_flag:
                age = competitive_table_sheet.cell_value(row_index,0)
                type1 = competitive_table_sheet.cell_value(row_index,1)
                type2 = competitive_table_sheet.cell_value(row_index,2)
                type3 = competitive_table_sheet.cell_value(row_index,3)
                type4 = competitive_table_sheet.cell_value(row_index,4)

                competitive_table.competitive_ability[age] = (type1, type2, type3, type4)

        return competitive_table

    def load_translocation_table(self, translocation_table_sheet):
        """
        loads the table with data on translocation
        """
        end_flag = True #used to let user customize number of rows in excel
                         #file by setting an END flag at the end of the table

        translocation_table = TranslocationTable()

        for row_index in range (self.STARTING_ROW, translocation_table_sheet.nrows):

            if translocation_table_sheet.cell_value(row_index,6) == 'END':
                end_flag = False

            elif end_flag:
                age = int(
                    translocation_table_sheet.cell_value(row_index,6)
                    )

                #control likelihoods
                control_male_likelihood = float(
                    translocation_table_sheet.cell_value(row_index,8)
                    )
                control_female_likelihood = float(
                    translocation_table_sheet.cell_value(row_index,7)
                    )
                #male biased likelihoods
                male_biased_male_likelihood = float(
                    translocation_table_sheet.cell_value(row_index,12)
                    )
                male_biased_female_likelihood = float(
                    translocation_table_sheet.cell_value(row_index,11)
                    )
                #female biased likelihoods
                female_biased_male_likelihood = float(
                    translocation_table_sheet.cell_value(row_index,16)
                    )
                female_biased_female_likelihood = float(
                    translocation_table_sheet.cell_value(row_index,15)
                    )

                translocation_table.control_translocation_likelihood[
                age] = (control_male_likelihood,
                    control_female_likelihood)

                translocation_table.male_biased_translocation_likelihood[
                age] = (male_biased_male_likelihood,
                    male_biased_female_likelihood)

                translocation_table.female_biased_translocation_likelihood[
                age] = (female_biased_male_likelihood,
                    female_biased_female_likelihood)

        return translocation_table
































