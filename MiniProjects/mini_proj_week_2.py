

#=============================================================
# This program allows the user to paly RPSLS game
# Date: Jun-5-2015             Class:Coursera_Python_I/week_2
#==============================================================




#-----Import - section-------
import random
#----------------------------


#------Functions-------------

def name_to_number(name):
    
       if name=="rock":
           nb = 0
       elif name == "spock":
           nb = 1
       elif name == "paper":
           nb = 2
       elif name == "lizard":
           nb = 3
       else: 
           nb = 4
       return nb


def number_to_name(nb):
    
      if nb == 0:
            name = "rock"
      elif nb == 1:
           name =  "spoke"
      elif nb == 2:
           name =  "paper"
      elif nb == 3:
           name = "lizard"
      else:
           name = "scissors"
        
      return name



def rpsls(player_choice): 
   
    print("")
    
    print "Player's choice is:",player_choice
    
    player_number =  name_to_number(player_choice)
    comp_number = random.randrange(0,5)
    comp_choice = number_to_name(comp_number)
    
    print "Computer's choice is:",comp_choice
    
    game_no = (comp_number - player_number)%5
    
    if (game_no == 4) or (game_no == 3):
        print("Computer wins!")
    elif (game_no ==1) or (game_no == 2):
        print("Player wins!")
    else: 
        print("Player and computer tie!")
    return



#=============  Test - Section  ===================    
rpsls("rock")
rpsls("spock")
rpsls("paper")
rpsls("lizard")
rpsls("scissors")
#===================================================




