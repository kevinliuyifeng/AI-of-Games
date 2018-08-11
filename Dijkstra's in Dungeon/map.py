import random

height = 100
width = 100
difficulty = 0
area = height * width
difficulty = area * difficulty / 100

x = []
y = []
walls = {}
waypoints = {}
spaces = {}
for diff in range(0, difficulty):
	x.append(random.randint(1, width-1))
	y.append(random.randint(1, height-1))
	walls[(x[diff],y[diff])] = 'X'

#waypoints[(random.randint(1, width-1), random.randint(1, height-1))] = 'a'
#waypoints[(random.randint(1, width-1), random.randint(1, height-1))] = 'c'
#print waypoints
for wall in range(0,height-1):
	walls[(0, wall)] = 'X'
	walls[(height-1, wall)] = 'X'
	walls[(wall, 0)] = 'X'
	walls[(wall, width-1)] = 'X'

level = {'walls': walls,
         'spaces': spaces
         }

print level
chars = []
for j in range(0, height-1):
	for i in range(0, width-1):
		cell = (i,j)
		if cell in level['walls']:
			chars.append(level['walls'][cell])
		#elif cell in level['waypoints']:
		#	chars.append(level['waypoints'][cell])
		else:
			chars.append('.')
	chars.append('\n')
#print ''.join(chars)


#print walls

txtName = "testmap.txt"
f=file(txtName, "a+")
f.write(''.join(chars))