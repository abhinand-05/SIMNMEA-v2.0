"""
Author: Bipal Shakya
Reading from excel file
"""

# ===============================================================================
# Imports
import sys, random  # , os, time
import datetime
from readTextFile import readTextFile

nmeaFormatValRefOldVer = readTextFile(3, './nmeaFormatValRef/nmeaFormatValRefOldVer')
nmeaFormatValRef = readTextFile(3, './nmeaFormatValRef/nmeaFormatValRef')

# ===============================================================================

# ===============================================================================
# Search for "Main Starts" to go to main logic
class NmeaSimulator:
    """
    talkerId        e.g.    AI, GP, HC, etc.
    sentenceId        e.g.    VDM, GGA, TTM, etc.
    sentenceFormat    e.g.
    """
    def main(self, talkerId, sentenceId, loopCount, chosenRouteFile, sentenceFormat, nmea_version):

        # ===============================================================================
        # Function blocks
        # ===============================================================================
        """
        sentenceHead        e.g.    $, !
        nmeaPlaceHolders    e.g.    llll.ll,a,yyyyy.yy,a,hhmmss.ss,A,a
        """
        def parseSentenceFormat(sentenceHead, nmeaPlaceHolders):
            baseSentence = ''
            placeHolderElem = []

            if nmea_version == '1.5':
                content = nmeaFormatValRefOldVer
            else:
                content = nmeaFormatValRef

            def getCheckSum(sentence):
                calc_cksum = 0
                for s in sentence:
                    calc_cksum ^= ord(s)
                return (str(hex(calc_cksum).lstrip('0x')).zfill(2)).upper()

            
            def adv_randomizer(baseSentence, placement):
                
                # For basic randomizer with basic conditions. The conditions are compared only
                # with the strings acquired from NMEA simulator's format reference and NOT 
                # the excel format
                # Remember to ALWAYS have unique cases earlier in the if conditions, and the 
                # relatively general conditions later in the if conditions so that unique 
                # conditions aren't missed out because it's returned by a general condition
                # instead

                

                def basic_randomizer(placeHolder):
                    switcher = {
                        'x':           random.randint(0,8),
                        'xx':          str(random.randint(1,12)).zfill(2),
                        'xxx':         str(random.randint(1,999)).zfill(3),
                        'x.x':         "%.2f" % random.uniform(0.0, 359.0),
                        'dd':          str(datetime.date.today().day).zfill(2),
                        'mm':          str(datetime.date.today().month).zfill(2),
                        'yyyy':        str(datetime.date.today().year).zfill(4),
                        'hhmmss.ss':   (datetime.datetime.utcnow().strftime("%H%M%S.%f"))[:9],
                        'ddmmyy':      str(datetime.date.today().day).zfill(2) + str(datetime.date.today().month).zfill(2) + (str(datetime.date.today().year).zfill(2))[2:],
                        'yyyymmdd':    (str(datetime.date.today().year).zfill(4)) + str(datetime.date.today().month).zfill(2) + str(datetime.date.today().day).zfill(2),
                        'hhmmss':      (datetime.datetime.utcnow().strftime("%H%M%S")),
                        'ccc':         'STR',
                        'c--c':        "AUT"
                    }
                    return switcher.get(placeHolder, '0')


                for each in content:
                    eachSId = each.split('-->')[0]
                    
                    if eachSId == sentenceId:
                        elemChoices = (((each.split(',', 1)[1]).split('*hh'))[0]).split(',')

                        basicRandom = basic_randomizer(elemChoices[placement])

                        if basicRandom == '0':
                            # ============================================================
                            # Inter elemency:
                            # ============================================================
                            global element_pointer
                            global zfillValue_round
                            global zfillValue
                            element_pointer = None

                            def inter_element():
                                global element_pointer

                                def get_mid_string(this_string, first, last):
                                    try:
                                        start = this_string.index(first) + len(first)
                                        end = this_string.index(last, start)
                                        return this_string[start:end]
                                    except ValueError:
                                        return 'PLACEHOLDER_ERR_IN_INTERELEMENT'

                                # haha. if 'if'. Funny.
                                if 'if(' in elemChoices[placement]:
                                    for this_if_oper in elemChoices[placement].split(';'):
                                        elem_index = get_mid_string(this_if_oper, 'element[', ']')
                                        elem_val = get_mid_string(this_if_oper, "=='", "')")

                                        if baseSentence.split(',')[int(elem_index)] == elem_val:
                                            return this_if_oper.split(':')[1]

                            # ==============================================================

                                if 'element[' in elemChoices[placement]:
                                    element_pointer = int(get_mid_string(elemChoices[placement], 'element[', ']'))

                                if element_pointer is not None:
                                    # Condition only for multiply application
                                    if ']*' in elemChoices[placement]:
                                        return str(round(float(baseSentence.split(',')[element_pointer]) * float(elemChoices[placement].split(']*')[1]), zfillValue_round)).zfill(zfillValue + 2)
                                return elemChoices[placement]

                            elemChoices[placement] = inter_element()

                            # ============================================================
                            # Range Condition
                            # ============================================================
                            if '-' in elemChoices[placement]:
                                rangeFrom, rangeTo = elemChoices[placement].split('-')

                                # Condition list within 'range' format
                                # A list of rules on the ranges before returning a randomized value
                                # replace 'neg' with -ve sign
                                if 'neg' in (rangeFrom or rangeTo):
                                    rangeFrom, rangeTo = rangeFrom.replace('neg', '-'), rangeTo.replace('neg', '-')
                                    
                                # This is to get the number of digits from the minimum range
                                zfillValue = len((rangeFrom.split('.')[0]).replace('-', ''))
                                    
                                if '.' in (rangeFrom):
                                    zfillValue_round = len(rangeFrom.split('.')[1])
                                    selected_random = str(round(random.uniform(float(rangeFrom), float(rangeTo)), zfillValue_round))
                                    if "-" in selected_random:
                                        # zfillValue increment to account for the negative symbol
                                        zfillValue = zfillValue + 1

                                    # zfillValue + 2 to account for the decimal point and single digit decimal number
                                    return selected_random.zfill(zfillValue + 2)
                                else:
                                    selected_random = str(random.randint(int(rangeFrom), int(rangeTo))).zfill(zfillValue)
                                    if "-" in selected_random:
                                        # zfillValue increment to account for the negative symbol
                                        zfillValue = zfillValue + 1

                                    return selected_random.zfill(zfillValue)



                            # ============================================================
                            # Or Condition
                            # ============================================================
                            elif '/' in elemChoices[placement]:
                                choice_list = elemChoices[placement].split('/')
                                return random.choice(choice_list)

                            else:
                                return elemChoices[placement]

                        return basicRandom

                    else:
                        continue



            # Third step (continuing from the main method), pour each comma delimited 
            # element of the actual informative sentence to a list
            placeHolderElem = nmeaPlaceHolders.split(',')
            
            # loop through each element of the nmea sentence
            lenPlaceHolderElem = len(placeHolderElem)
            elemNum = 0
            while (elemNum < lenPlaceHolderElem):
                # Take special consideration for lat/long elements of nmea sentence
                if placeHolderElem[elemNum] == 'llll.ll':
                    baseSentence = baseSentence + str(latlongRouteLoop(loopCount))
                    # Jump three indexes of the list because latlong is a four-index
                    #    long response which is triggered by the first index "llll.ll"
                    #    but returns randomized values for all four indexes:
                    #    llll.ll,a,yyyy.yy,a
                    elemNum += 3
                else:
                    baseSentence = baseSentence + str(adv_randomizer(baseSentence, elemNum)) + ","
                elemNum += 1

            if talkerId != sentenceId:
                finalSentence = str(talkerId + sentenceId + "," + baseSentence[:-1])
            else:
                finalSentence = str(talkerId + "," + baseSentence[:-1])

            if talkerId == 'LC':
                finalSentence = finalSentence[2:]

            return sentenceHead + finalSentence + "*" + str(getCheckSum(finalSentence))


        # For longitude and latitude
        def latlongRouteLoop(lineToGet):
            # Open the previously randomly selected route file
            with open(chosenRouteFile) as f:
                routeList = [line.rstrip() for line in f]
            # Line to get is subtracted by 1 because we're reading a list, therefore,
            # list index is equal to line number - 1
            return (routeList[lineToGet-1] + ",")
            
        # ===============================================================================
        # ===============================================================================
        # ===============================================================================
        # Main Starts
        # ===============================================================================
        # ===============================================================================
        # ===============================================================================

        if sentenceFormat == '0':
            return None

        if sentenceFormat == None:
            return None

        # REMOVING irrelevant information from the raw sentence got from reading the
        # intersected information from excelsheet above:
        # First step, checksum from the raw sentence
        # fs_ prefix to represent first step.
        fs_head = (sentenceFormat.partition('*hh'))[0]
        # Second step, remove header from the above partioned sentence; and have it
        # separated from the required raw sentence format (in the following case,
        # ss_tail). ss_ prefix to represent second step.
        ss_head, ss_sep, ss_tail = fs_head.partition(',')
        
        # Pass only the required elements (irrelevant elements of the raw
        # sentence removed above in First and Second steps) of the NMEA
        # sentence format to the parsing sub-routine which will replace
        # base sentence's placeHolders with random but valid values

        # Call sent out to parseSentenceFormat() for each loop, so that each
        # loop outputs random but valid value for the elements of the raw
        # sentence format.
        # PS: ss_head[0] is the header character of any sentence, borrowed
        # from raw sentence format for simulation.

        return parseSentenceFormat(ss_head[0], ss_tail)

if __name__ == "__main__":
    print ("Sorry. This module cannot be run directly. Try running: python __init__.py instead.")
    sys.exit()
