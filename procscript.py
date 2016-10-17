#!/usr/bin/python

from enigma.machine import EnigmaMachine
import itertools #library for creating combinations/permutations
from multiprocessing import Pool #threading ftw

#possible settings we don't know
ALLROTORS = [("I", "II", "III"),("II", "I", "III"),("III", "II", "I"),("II", "III", "I"),("III", "I", "II"),("I", "III", "II")]
ALLPAIRS = itertools.combinations("AEGINVXZ", 2)
ALLREFLECTORS = ['B', 'C', 'B-Thin', 'C-Thin']
ALLRINGS = itertools.permutations(range(0,26) ,3)

def enigma_thang(rGuessIn, reflect_In, pairG_In, rSettings):
	#we are given these settings
    initkey = 'GQT'
    messagekey='UKJ'
    ciphertext = 'GCXSSBPPIUDNWXJZGIICUEFYGISQOCGLLGMMKYHJ'
    
    rguess= rGuessIn
    pairguess = pairG_In

	#initiate machine with known quantities and guesses
    machine = EnigmaMachine.from_key_sheet(
        rotors="{} {} {}".format(rguess[0], rguess[1], rguess[2]),
        reflector=reflect_In,
        ring_settings=rSettings,
        plugboard_settings='BF CM DR HQ JK LU OY PW ST {}'.format(pairguess),
        )

    #encrypt the message key so we can use decrypted key as display for next round
    machine.set_display(initkey)
    msg_key = machine.process_text(messagekey)

	#finally decrypt with all settings set up
    machine.set_display(msg_key)
    plaintext = machine.process_text(ciphertext)

	#check if we are close to correct so we don't wait 10 minutes to figure out code is wrong
    if "ELADE" in plaintext:
        print (plaintext,rGuessIn, reflect_In, pairG_In, rSettings)
        print ("THIS ONE!!!!!!!!!!!!!!!!!!!!")

if __name__ == "__main__":
    p = Pool(8)
    
    ALLPAIRSTUPLE = tuple(ALLPAIRS)
    #for the purposes of demonstration
    print (ALLPAIRSTUPLE[0]) #print first pair
    print (ALLPAIRSTUPLE[0][0] + ALLPAIRSTUPLE[0][1]) #convert first pair to string form
    
    """
    #slower, traditional method
    params = []
    i = 0
    for c in ALLREFLECTORS: #most likely B so we iterate over these last
        for pair in ALLPAIRSTUPLE:
            for r in ALLROTORS:
                for perm in itertools.permutations(range(0,26) ,3):
                    params.append(tuple((r, c, pair[0]+pair[1], list(perm))))
                    i +=1
    print(len(params))
    p.starmap(enigma_thang, params)
    """
    
    #faster, more "pythonic" but equivalent to params
    paramscomprehension = [(r, refl, pair[0]+pair[1], list(perm)) for refl in ALLREFLECTORS for perm in ALLRINGS for r in ALLROTORS for pair in ALLPAIRSTUPLE]
    print (len(paramscomprehension))
    p.starmap(enigma_thang, paramscomprehension)

	#probably the best thing to do would be to make a generator function but w/e
    p.close()
    p.join()
