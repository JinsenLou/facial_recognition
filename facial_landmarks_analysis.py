'''
Finished Date: 2022-10-07
This program is to read the csv file and print the information of the subjects.
It mainly includes 5 sections: the first section is to read the csv file and form
a 3 layers dictionary, which provides the basic data structure for the rest of four
sections; the second section is to calculate the asymmetry between the original and 
mirrored face for the landmarks; the third section is to claculate 3D Euclidean distance 
between the corresponding landmarks; the fourth section is to get 5 faces having 
the lowest total face asymmetry; the fifth section is to calculate the cosine similarity 
between the 2 faces mentioned in the list of subjIDs.
'''

def read_file(csvfile):
    '''
    This function is to read the csv file and form a 3 layers dictionary, The first layer is the subject ID,
    the second layer is the landmark, and the third layer is the coordinate, including x, y, and z for the
    original face and the mirrored face.This top dictionary provides the basic data structure for the rest
    of the program. It looks like {SUBJID:{LANDMARKS:{COORDINATE_NAME:COORDINATE,...}}}
    '''
    # open the csv file and read the data
    try:
        file = open(csvfile, "r")
    except: # if the file is not found or can't be opened, return None
        print("The provided filename is either wrong or is not permitted to be read.")
        return None

    try: # if the header of the file is wrong or missing partly, return None
        header = file.readline().strip().split(",")

        # read the header of the csv file and strip the blank space and split them by comma
        for i in range(len(header)):
            header[i] = header[i].upper() # change the header to upper case

        inx_dict = {}
        # a dictionary to store the index for each attribute incase the order of the headers is changed
        ordered_headers = ["SUBJID", "LANDMARK", "OX", "OY", "OZ", "MX", "MY", "MZ"]
        for h in ordered_headers:
            inx_dict[h] = header.index(h)
    except:
        return None

    lst_corrupted_ID = [] # a list to store the IDs of the corrupted data
    top_dict = {} # read the data from the csv file and store them in a three layer dictionary
    for row in file:
        row = row.strip().split(",")
        row = [x.upper() for x in row if isinstance(x, str)] # convert all the strings to upper case
        ID = row[inx_dict["SUBJID"]]
        landmark = row[inx_dict["LANDMARK"]] # get the landmark
        if landmark == "":
            lst_corrupted_ID.append(ID)
            continue
        if ID not in top_dict: # if the subject ID is not in the dictionary, add it
            top_dict[ID] = {}
        top_dict[ID][landmark] = {}
        for h in ordered_headers[2:]: # the ordered coordinates are from the 3rd to the 8th
            coordinate = row[inx_dict[h]]
            if coordinate == "": # if the coordinate is empty, then it's corrupted data
                lst_corrupted_ID.append(ID)
                continue
            coordinate = float(coordinate)
            if coordinate >= 200 or coordinate <= -200: # if the coordinate is out of the range(-200, 200), then it's corrupted data
                lst_corrupted_ID.append(ID)
                continue
            top_dict[ID][landmark][h] = coordinate
    file.close() # close the file after reading the data and storing them in the dictionary

    # remove the corrupted data from the dictionary
    for ID in lst_corrupted_ID:
        if ID in top_dict:
            del top_dict[ID]
    return top_dict


def calc_asymmetry(ID, top_dict):
    '''
    This function is to calculate the asymmetry of a subject. First the difference between the
    original and mirrored coordinates is calculated, and then get the sum of the squares of the
    differences, finally it's used to get the square root which is the asymmetry.
    '''
    sub_dict = top_dict[ID]
    op1_dict = {}

    for landmark in sub_dict:
        dif1 = sub_dict[landmark]["MX"] - sub_dict[landmark]["OX"]
        dif2 = sub_dict[landmark]["MY"] - sub_dict[landmark]["OY"]
        dif3 = sub_dict[landmark]["MZ"] - sub_dict[landmark]["OZ"]
        assmmetry = (dif1**2 + dif2**2 + dif3**2)**0.5
        op1_dict[landmark] = assmmetry

    if op1_dict["PRN"] != 0:
    # The PRN represents the nose tip, so its asymmetry must be 0, if not, it's wrong. here
    # if the asymmetry of the PRN is not 0, then return None to indicate that the subject is not valid
        for lanmark in op1_dict:
            op1_dict[lanmark] = None
            del op1_dict["PRN"] # delete the PRN from the dictionary
        return op1_dict
    else:
        del op1_dict["PRN"] # delete the PRN from the dictionary
        return op1_dict

def OP1(top_dict, SubjIDs):
    '''
    This function is to get the asymmetry for each face in the given subject IDs. The calc_asymmetry
    function defined above calculate the asymmetry, and store it in a dictionary and the result
    is returned as a list.
    '''
    lst_op1 = []
    for ID in SubjIDs:
        if ID not in top_dict: # if the subject ID is not in the dictionary, then it's invalid and return None
            lst_op1.append(None)
        else:
            op1_dict = calc_asymmetry(ID, top_dict)
            for k in op1_dict: # get the asymmetry for each face and round it to 4 decimal places
                asymetry = round(op1_dict[k], 4)
                op1_dict[k] = asymetry
            lst_op1.append(op1_dict)
    return lst_op1

def calc_distance(top_dict, ID, landmark1, landmark2):
    '''
    This function is to calculate the distance between two landmarks on the original face.
    '''
    sub_dict = top_dict[ID]
    dif1 = sub_dict[landmark2]["OX"] - sub_dict[landmark1]["OX"]
    dif2 = sub_dict[landmark2]["OY"] - sub_dict[landmark1]["OY"]
    dif3 = sub_dict[landmark2]["OZ"] - sub_dict[landmark1]["OZ"]
    distance = (dif1**2 + dif2**2 + dif3**2)**0.5
    return round(distance, 4)

def OP2(top_dict, SubjIDs):
    '''
    This function is to get six 3D Euclidean Distances on the original face for
    each face in the given subject IDs. The 6 distances are the distances between
    the following landmarks:
    1.EXEN: Ex En 2.ENAL: En Al 3.AlEX: Al Ex 4.FTSBAL: Ft Sbal 5.SBALCH: Sbal Ch 6.CHFT: Ch Ft
    The result is presented as dictionaries inside a list.
    '''
    lst_op2 = []
    for ID in SubjIDs:
        if ID not in top_dict: # if the ID is not in the dictionary, return None
            lst_op2.append(None)
        else: # if the ID is in the dictionary, calculate the distances and store them in a dictionary
            sub_dict = {}
            sub_dict["EXEN"] = calc_distance(top_dict, ID, "EX", "EN")
            sub_dict["ENAL"] = calc_distance(top_dict, ID, "EN", "AL")
            sub_dict["ALEX"] = calc_distance(top_dict, ID, "AL", "EX")
            sub_dict["FTSBAL"] = calc_distance(top_dict, ID, "FT", "SBAL")
            sub_dict["SBALCH"] = calc_distance(top_dict, ID, "SBAL", "CH")
            sub_dict["CHFT"] = calc_distance(top_dict, ID, "CH", "FT")
            lst_op2.append(sub_dict)
    return lst_op2

def OP3(top_dict):
    '''
    This function is to firstly calculate total asymmetries of each subject in the csv file
    using the calc_asymmetry function defined above, and then return a tuple of the 5 faces
    having the lowest total face asymmetry.
    The first member of each tuple is the “SubjID” of the face while the second member is
    the total asymmetry of this face and the list is sorted in ascending order.
    '''
    lst_op3 = []
    for ID in list(top_dict.keys()):
        sum_asymmetry = round(sum(calc_asymmetry(ID, top_dict).values()), 4)# calculate the total asymmetry
        lst_op3.append((ID, sum_asymmetry))
    lst_op3.sort(key=lambda x: x[1]) # sort the list by the total asymmetry
    return tuple(lst_op3[:5])

def OP4(top_dict, SubjIDs):
    '''
    This function is to calculate the cosine similarity between faces F1 and F2 from
    the subjIds list based on the dictionary of six distances calculated in OP2.
    '''
    if SubjIDs[0] in top_dict and SubjIDs[1] in top_dict:
        distances = OP2(top_dict, SubjIDs)
        dict_f1 = distances[0]
        dict_f2 = distances[1]
        numerator = 0
        denominator1 = 0
        denominator2 = 0
        for key in dict_f1: # use the same key of the two dictionaries to get the parts of cosine similarity
            numerator += dict_f1[key] * dict_f2[key]
            denominator1 += dict_f1[key] ** 2
            denominator2 += dict_f2[key] ** 2
        denominator = (denominator1 ** 0.5) * (denominator2 ** 0.5)
        return round(numerator / denominator, 4)
    else:
        return None

def main(csvfile, SubjIDs):
    '''
    This main function is to call all the functions above and return all the results. Before calling the functions,
    the parameters are checked to make sure they are valid.
    '''
    if type(SubjIDs) != list: # check if the SubjIDs is a list
        return None, None, None, None
    if len(SubjIDs) != 2: # check if the length of the SubjIDs is 2
        return None, None, None, None

    top_dict = read_file(csvfile)
    if top_dict is None: # check if the csv file is valid
        return None, None, None, None

    for ID in SubjIDs:
        if type(ID) != str: # check if the elements in the SubjIDs are strings
            return None, None, None, None
        
    # convert the SubjIDs to upper case for all letters
    SubjIDs = [ID.upper() for ID in SubjIDs]
    
    return OP1(top_dict, SubjIDs), OP2(top_dict, SubjIDs), OP3(top_dict), OP4(top_dict, SubjIDs)

# This is the end of the program, thank you for reading!

