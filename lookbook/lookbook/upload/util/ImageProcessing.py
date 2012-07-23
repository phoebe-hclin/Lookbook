# /usr/bin/python

import math
from operator import itemgetter
from PIL import Image

def read_image(filename):
	im = Image.open(filename)
	if im:
		return im
	else:
		print 'Failed to open the file'
		return None

def get_avg_rgb(pixels, px_start, px_end, py_start, py_end):
	sum_r = 0
	sum_g = 0
	sum_b = 0
	total_pixels = (py_end - py_start) * (px_end - px_start)

	for y in range(py_start, py_end):
		for x in range(px_start, px_end):
			r, g, b = pixels[x, y]
			sum_r += r
			sum_g += g
			sum_b += b
	return (sum_r/total_pixels, sum_g/total_pixels, sum_b/total_pixels)

def get_grid_colors(im=None, step=2):
	pixels = im.load()
	image_size_x, image_size_y = im.size
	grid_size_x = image_size_x / step
	grid_size_y = image_size_y / step

	default_rgb = (-1, -1, -1)

	grids = [[default_rgb for x in range(grid_size_x)] for y in range(grid_size_y) ]
	for y in range(grid_size_y):
		py_start = y * step
		py_end = py_start + step
		if y == grid_size_y - 1:
			py_end = image_size_y
		for x in range(grid_size_x):
			px_start = x * step
			px_end = px_start + step
			if x == grid_size_x - 1:
				px_end = image_size_x
			grids[y][x] = get_avg_rgb(pixels, px_start, px_end, py_start, py_end)

	#print grids
	#print im.size
	#print grid_size_x, grid_size_y
	return (grids, grid_size_x, grid_size_y)

def rgb2hue(rgb):
	r, g, b = rgb
	hue = 180 / math.pi * math.atan2(math.sqrt(3)*(g-b), 2*r-g-b)
	if hue < 0:
		hue += 360
	return hue

def hue2bin(hue, bin_step):
	b = int(hue) / bin_step
	if b == 360 / bin_step:
		b -= 1 
	return b

def hue2bin2(hue):
	if ((hue < 30) or (hue > 345)):
		return 0
	elif (hue < 45):
		return 1 # orange
	elif (hue < 75):
		return 2 # yellow
	elif hue < 165:
		return 3 # green
	elif hue < 210:
		return 4 # green-blue
	elif hue < 270:
		return 5 # blue]
	elif hue < 285:
		return 6 # purple
	elif hue < 346:
		return 7 # purple red
	
	
	

def get_grid_hue(grids_rgb, grid_size_x, grid_size_y):
	grids_hue = [[-1 for x in range(grid_size_x)] for y in range(grid_size_y) ]
	for y in range(grid_size_y):
		for x in range(grid_size_x):
			grids_hue[y][x] = rgb2hue(grids_rgb[y][x])
	return grids_hue

def get_grid_bin(grids_rgb, grid_size_x, grid_size_y):
	grids_bin = [[-1 for x in range(grid_size_x)] for y in range(grid_size_y) ]
	for y in range(grid_size_y):
		for x in range(grid_size_x):
			hue = rgb2hue(grids_rgb[y][x])
			grids_bin[y][x] = hue2bin(hue, 36) #hue2bin
	return grids_bin

def bin_thresholding(grids_bin, grid_size_x, grid_size_y, bin_step):
	bin_size = 360 / bin_step
	bin_count = [0 for b in range(bin_size)]
	for y in range(grid_size_y):
		for x in range(grid_size_x):
			bin_count[grids_bin[y][x]] += 1
	return bin_count

def find_typical_colors(bin_count):
	bin_tuples = []
	for b in range(len(bin_count)):
		bin_tuples.append((b, bin_count[b]))
	best_bin_tuples = sorted(bin_tuples, key=itemgetter(1), reverse=True)[0:3] #find the first 3 colors
	best_bin_list = [b for (b, count) in best_bin_tuples]
	return best_bin_list

def best_matched_colors(filename=None):
	im = read_image(filename)
	grids_rgb, grid_size_x, grid_size_y = get_grid_colors(im, 10)
	grids_bin = get_grid_bin(grids_rgb, grid_size_x, grid_size_y)
	bin_count = bin_thresholding(grids_bin, grid_size_x, grid_size_y, 36)
	return find_typical_colors(bin_count)

