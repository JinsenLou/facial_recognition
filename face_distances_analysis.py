"""
This is a program about the analysis of Face recognition (FR), it is to help the researchers in analysing 
eight geodesic (surface) (GDis in the file )and eight 3D Euclidian distances(LDis in the file)
between a few facial landmarks across four expressions 'Neutral', 'Angry', 'Disgust', 'Happy'. 
These distances on one face (in Neutral expression) can then be used to calculate cosine similarity with the same face 
in different expressions and with other faces in the data set to see which faces are closer to (or look like) the reference face.
There are 5 columns in the file, the 1st is the adultID, 2nd is the Expression, 3rd is the 8 different distances reference,
representing by the number from 1-8, 4th is the GDis and 5th is the Ldis.
"""

def main(csvfile, adultID, Option):
    #Firstly open the file and read the data
    lines = []
    with open(csvfile, "r") as filein:
        for line in filein:
            linelist = line[:-1].split(",")
            lines.append(linelist)
            
        #Firstly is to find out in which lines the adultID are.
        def get_lines_inx(adultID):
            #This function is to get the index of the lines where the adultID is the same
            list_inx_lines = []
            for inx in range(len(lines)):
                    if adultID in lines[inx]:
                        list_inx_lines.append(inx)  
            return list_inx_lines

        """
        This section is to calculate the minimum (non-zero) maximum GDis
        and LDis of each distance across the four expressions for OP1 when the
        option equals to 'stats'.
        The first 2 functions are created to get the gdis and ldis of by using
        the adultID and the distance. The third function is to get the min and max
        of the gdis and ldis of each distance. Finnaly, by converting the range(1,9)
        into string, the min and max of each distance can be returned.
        """    
        def get_gdis(adultID, distance):
            #This function is to get the list of gdis of certain distance
            list_inx_lines = get_lines_inx(adultID)
            lines_of_adultID = lines[list_inx_lines[0]:list_inx_lines[-1] +1]
            list_gdis = []
            for l in lines_of_adultID:
                if l[2] == distance:
                    gdis = round(float(l[3]),4)
                    if gdis <= 0:
                        gdis = 50.0 #If the gdis is negative or 0, then set it to 50
                    list_gdis.append(gdis)
            return list_gdis
        
        def get_ldis(adultID, distance):
            #This function is to get the index of the lines where the adultID is the same
            list_inx_lines = get_lines_inx(adultID)
            lines_of_adultID = lines[list_inx_lines[0]:list_inx_lines[-1] +1]
            list_ldis = []
            for l in lines_of_adultID:
                if l[2] == distance:
                    ldis = round(float(l[4]),4)
                    if ldis <= 0:
                        ldis = 50.0 #If the ldis is negative or 0, then set it to 50
                    list_ldis.append(ldis)
            return list_ldis
            
            
        def get_list_min_max(adultID, distance):
            #calculate the OP1, OP2, OP3, OP4
            list_gdis = get_gdis(adultID, distance)
            list_ldis = get_ldis(adultID, distance)
            minGDis = min(list_gdis)
            maxGDis = max(list_gdis)
            minLdis = min(list_ldis)
            maxLdis = max(list_ldis)
            list_min_max = [minGDis , maxGDis, minLdis, maxLdis]
            return(list_min_max)
        
        
        def OP1(adultID):
            #OP1 is A list of lists containing the minimum (non-zero) maximum GDis
            #and LDis of each distance across the four expressions.
            list_op1 = []
            dis = 1
            for dis in range(1,9):
                list_min_max = get_list_min_max(adultID, str(dis))
                list_op1.append(list_min_max)
                dis += 1
            return list_op1
        
        """
        This section is to get the list of gdis and ldis according to the order of the distance
        from 1- 8, because there are some of distance data are not listed in the right oder.
        the 2 getting list functions will be used for all the rest of outputs
        """
        
        def get_exp_line_inx(adultID, expression):
            #This function is to get the index of certain expression for certain adultID
            list_exp_inx = []
            list_inx_lines = get_lines_inx(adultID)
            for inx in range(len(lines)):
                if expression in lines[inx] and list_inx_lines[0] <= inx <= list_inx_lines[-1]:
                    list_exp_inx.append(inx)
            return list_exp_inx
      

        def get_gdis_list(adultID, expression = "Neutral"):
            #This function is to get the gdis list in order for certain expression for certain adultID using the function get_gdis_exp
            list_gdis = []
            def get_gdis_exp(adultID, dis, expression):
            #This function is to get the gdis for certain expression for certain adultID, and the default expression is "Neutral"
                list_exp_inx = get_exp_line_inx(adultID, expression)
                lines_of_exp = lines[list_exp_inx[0]:list_exp_inx[-1]+1]
                global gdis
                for l in lines_of_exp:
                    if l[1] == expression and l[2] == dis:
                        gdis = float(l[3])
                        return gdis
            dis = 1
            for dis in range(1,9):
                gdis = get_gdis_exp(adultID, str(dis), expression)
                if gdis <= 0:
                    gdis = 50 #If the gdis is negative or 0, then set it to 50
                list_gdis.append(gdis)
                dis += 1
                
            return list_gdis
        

        def get_ldis_list(adultID, expression):
            #This function is to get the gdis list in order for certain expression for certain adultID using the subfunction get_gdis_exp
            list_ldis = []
            def get_ldis_exp(adultID, dis, expression):
            #This sub_function is to get the gdis for certain expression for certain adultID, and the default expression is "Neutral"
                list_exp_inx = get_exp_line_inx(adultID, expression)
                lines_of_exp = lines[list_exp_inx[0]:list_exp_inx[-1]+1]
                for l in lines_of_exp:
                    if l[1] == expression and l[2] == dis:
                        ldis = float(l[4])
                        return ldis   
            dis = 1
            for dis in range(1,9):
                ldis = get_ldis_exp(adultID, str(dis), expression)
                if ldis <= 0:
                    ldis = 50 #If the ldis is negative or 0, then set it to 50
                list_ldis.append(ldis)
                dis += 1
            return list_ldis
        
           
        def OP2(adultID):
            list_op2 = []
            # create an empty list to store the differences
            def get_dif_gdis_ldis(adultID, expression):
            #This sub_function is to get the difference between gdis and ldis
                list_gdis = get_gdis_list(adultID, expression)
                list_ldis = get_ldis_list(adultID, expression)
                list_gdis_ldis_dif = []
                i = 0
                for gdis in list_gdis:
                    for ldis in list_ldis:
                        dif = list_gdis[i] - list_ldis[i]
                    dif = round(dif, 4)
                    list_gdis_ldis_dif.append(dif)
                    i += 1
                return list_gdis_ldis_dif
            
            exps = ["Neutral","Angry","Disgust","Happy"]
            for exp in exps:
                    list_gdis_ldis_dif = get_dif_gdis_ldis(adultID, exp)
                    list_op2.append(list_gdis_ldis_dif)
            return list_op2
        
        
        def OP3(adultID):
            #This function is to calculate the average of the gdis for each distance.
            # OP3 using the function get_gdis
            list_op3 = [] # create an empty list to store the average of the gdis
            dis = 1
            for dis in range(1,9):
                list_gdis = get_gdis(adultID, str(dis))
                avg_gdis = sum(list_gdis)/len(list_gdis)
                list_op3.append(round(avg_gdis,4))
                dis += 1
            return list_op3
          
        
        def OP4(adultID):
            #This function is to calculate the standard deviation of the gdis for each distance.
            list_op4 = []
            def calc_std(adultID, distance): #define a function to calculate the standard deviation
                list_ldis = get_ldis(adultID, distance)
                mean = sum(list_ldis)/len(list_ldis)
                sum_diff = 0.0
                i = 1
                for i in range(4):
                    sum_diff += (list_ldis[i]- mean)**2
                    i += 1
                std = (sum_diff/len(list_ldis))**0.5
                return round(std,4)
            #Then use the function to calculate std for each distance by looping the distance from 1 to 8
            dis = 1
            for dis in range(1,9): 
                std = calc_std(adultID, str(dis))
                list_op4.append(std)
                dis += 1
            return list_op4
        
        
        """
        This is the second part of the main function when the Option equals to "FR", 
        which means the user wants to get the facial recognition result by the the cosine similarity.
        It designs subfunctions for calculating the cos_sim inside of the adultID, which is 
        between the neutral expression and the other three expressions, secondly, the cos_sim of the 
        given adultID and the other adultIDs just in terms of the neutral expression.
        After that, it will compare the cos_sim of the given adultID inside and outside of the adultID,
        getting the biggest cos_sim inside and its adultID. It could be the different adultID, or the same adultID.
        """
       
        def calc_cos_sim(l1, l2):
        #Firstly define a function to calculate the cosine similarity between two lists,
        #and the defaulted list2- l2 is the list_gdis_neutral_givenID, because all the
        #cos_sim will be calculated based on this
            list_gdis_neutral_givenID = get_gdis_list(adultID)
            l2 = list_gdis_neutral_givenID
            sum_multi_gdis = 0.0
            sqrt1 = 0.0
            sqrt2 = 0.0
            for i in range(8):
                sum_multi_gdis += l1[i] * l2[i]
                sqrt1 += l1[i]**2
                sqrt2 += l2[i]**2
                cos_sim = sum_multi_gdis/(sqrt1*sqrt2)** 0.5
            return round(cos_sim,4)
        
        
        def calc_cos_sim_in(adultID):
        #This function is to calculate the cosine similarity between the expression "Neutral" of adultID
        #and the other 3 expressions of the given adultID and get the biggest one in 3.
            list_gdis_neutral = get_gdis_list(adultID)
            list_gdis_angry = get_gdis_list(adultID, "Angry")
            list_gdis_disgust = get_gdis_list(adultID, "Disgust")
            list_gdis_happy = get_gdis_list(adultID, "Happy")
            
            cos_sim_angry = calc_cos_sim(list_gdis_angry, list_gdis_neutral)
            cos_sim_disgust = calc_cos_sim(list_gdis_disgust, list_gdis_neutral)
            cos_sim_happy = calc_cos_sim(list_gdis_happy, list_gdis_neutral)
            list_cos_sim = [cos_sim_angry, cos_sim_disgust, cos_sim_happy]
            max_cos_sim = max(list_cos_sim)
            return max_cos_sim
   
        
        def calc_cos_sim_neu(adultID):
            #This function is to calculater the cosine similarity of neutral expression
            #between the given ID and all the adultIDs, outputting the biggest one.
            list_cos_sim_neu = []
            list_gdis_neutral_givenID = get_gdis_list(adultID)
            #This part is to get the aultID list without the given adultID
            list_adultID = []
            for inx in range(1, len(lines)):
                adultID2 = lines[inx][0]
                list_adultID.append(adultID2)

            l_no_repeat = [] #create a list to store the adultID without repeat
            for i in list_adultID:
                if i not in l_no_repeat:
                    l_no_repeat.append(i)
            #This part is to get the gdis list of Neutral expression for each adultID
            for a_ID in l_no_repeat:
                list_gdis_neutral = get_gdis_list(a_ID)
                cos_sim_neu = calc_cos_sim(list_gdis_neutral, list_gdis_neutral_givenID)
                list_cos_sim_neu.append(cos_sim_neu)

            #Before calculating the cosine similarity, we need to get rid of the given adultID in parameter and its cosine similarity.
            max_cos_sim_neu = max(list_cos_sim_neu)
            inx = list_cos_sim_neu.index(max_cos_sim_neu)
            adID1 = l_no_repeat[inx]
            l_no_repeat.remove(adID1)
            list_cos_sim_neu.remove(max_cos_sim_neu)

            #This part is to get the biggest cosine similarity between the given adultID and the rest of the adultIDs
            max_cos_sim_neu = max(list_cos_sim_neu)
            inx = list_cos_sim_neu.index(max_cos_sim_neu)
            adID = l_no_repeat[inx] #get the adultID with the biggest cosine similarity
            list_return =[max_cos_sim_neu, adID]
            return list_return

        def cossim(adultID):
            #This function is to get the maximum cosine similarity between the expression "Neutral" of adultID and the other 3 expressions of adultID as
            #well as the other subjcts.
            max_cos_sim_in = calc_cos_sim_in(adultID)
            list_return1 = calc_cos_sim_neu(adultID)
            max_cos_sim_neu = list_return1[0]
            cossim = max(max_cos_sim_in, max_cos_sim_neu)
            return cossim

        def ID(adultID):
            #This function is to get the adultID of the other subject with the maximum cosine similarity between the expression "Neutral" of adultID and the other 3 expressions of adultID as
            #well as the other subjcts.
            max_cos_sim_in = calc_cos_sim_in(adultID)
            list_return1 = calc_cos_sim_neu(adultID)
            max_cos_sim_neu = list_return1[0]
            adID = list_return1[1]
            if max_cos_sim_in > max_cos_sim_neu:
                return adultID
            else:
                return adID
            
        """
        This last section is to finalise the result. It will return the OP1, OP2, OP3，OP4 when the third parameter is "stats".
        It will return the adultID with biggest cosine similarity when the third parameter is "FR". the ID could be the same as the given adultID
        when the cosine similarity between the expression "Neutral" of adultID and the other 3 expressions of adultID is bigger than 
        the cosine similarity between the expression "Neutral" of adultID and other subjects.
        """
        
        if Option == "stats":
            return OP1(adultID), OP2(adultID), OP3(adultID), OP4(adultID)
        elif Option == "FR":
            return ID(adultID), cossim(adultID)
        
#This is the end of the program.