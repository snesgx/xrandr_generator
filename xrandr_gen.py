import subprocess
result = subprocess.run(['xrandr'], stdout=subprocess.PIPE)

output = ''
primary = False
res_and_pos = ''
resolution = ''
position = ''
rotation = ''
refresh_rate = ''
finalcommandline = 'xrandr '
completedParsing = False

for line in result.stdout.decode('utf-8').split('\n'):
	if (' connected ' in line.lower()):
		output = line[:line.find(' ')]
		line = line[:line.find('(')].lower()
		primary = ' primary ' in line
		rotation = ' --rotate left ' if 'left' in line else ''
		for attr in line.split(' '):
			if ('x' in attr and '+' in attr):
				res_and_pos = attr.split('+')
				position = res_and_pos[1] + 'x' + res_and_pos[2]
	elif (output != ''):
		if ('*+' in line):
			for hz in line.split(' '):
				if '*' in hz:
					refresh_rate = hz.replace('*','').replace('+','')
					completedParsing = True
				elif 'x' in hz:
					resolution = hz
		if completedParsing:
			if position != '':
				finalcommandline += ' --output ' + output + (' --primary ' if primary else '') + ' --mode ' + resolution + rotation + ' --pos ' + position + ' -r ' + refresh_rate
			else:
				finalcommandline += ' --output ' + output + ' --off'
			output = ''
			primary = False
			res_and_pos = ''
			resolution = ''
			position = ''
			rotation = ''
			refresh_rate = ''

print (finalcommandline.replace('  ', ' '))
