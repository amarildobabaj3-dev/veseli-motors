import time
import os
Topi = "⚽"
pozicioni = 0
drejtimi = 1
while True:
	# 1.kjo fshin ekranin qe te mos mbushet me rreshta
	os.system('cls' if os.name == 'nt' else 'clear')
	#2.vizatoni objektin me hapesira perpara
	print(" " * pozicioni + Topi)
	#3. Ndryshoni pozicionin 
	pozicioni += drejtimi 
	#4. Nese prek fundin e ekranit,kthehu
	if pozicioni == 30 or pozicioni == 0:
		drejtimi *= -1
	#5. Sa sekonda te prese para se te levizi perseri
	time.sleep(0.09)