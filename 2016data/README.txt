A Hearthstone matche is built this way :

-turns : array
-the result of the matche for the player : str

A turn is composed of :
-the number of the turn
 : int
-cards played by current player : array
-current player : str
-health for player "me" : int
-health for player "opponent" : int
-armor for player "me" : int	
-armor for player "opponent" : int	
-number of card in the hand of player "me" : int	
-number of card in the hand of player "opponent" : int
		
-cards played by "me" still in the game : array	
-cards played by "opponent" still in the game : array	

Caution : turn 1 is always a turn you have to delete. Because it isn't a real turn