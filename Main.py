import pygame
import random
import math
import time
import tracemalloc
import psutil
pygame.init()

class DrawInformation:
	BLACK =0,0,0
	WHITE = 255,255,255
	GREEN = 0,255,0
	RED = 255,0,0
	BLUE = 0,0,255
	BACKGROUD_COLOR = WHITE

	GRADIENTS = [# diifrenet gradiant colour of gray
		(128,128,128),
		(160,160,160),
		(192,192,192)

	]

	FONT = pygame.font.SysFont('comicsans',20)
	LARGE_FONT = pygame.font.SysFont('comicsans',40)
	SIDE_PAD = 100 
	TOP_PAD = 150

	def __init__(self,weidth,heigth,lst):

		self.weidth = weidth
		self.heigth = heigth


		self.window = pygame.display.set_mode((weidth,heigth))

		pygame.display.set_caption("Sorting Alogrithm Visualization")
		self.set_list(lst)


	def set_list(self,lst):
		self.lst = lst
		self.min_value = min(lst)
		self.max_value = max(lst)

		self.block_weidth = round((self.weidth - self.SIDE_PAD)/ len(lst))
		# self.block_height = math.floor((self.heigth - self.TOP_PAD)/(self.max_value - self.min_value))
		range_of_values = self.max_value - self.min_value
		if range_of_values == 0:
			range_of_values = 1
		self.block_height = math.floor((self.heigth - self.TOP_PAD)/range_of_values)
		self.start_x = self.SIDE_PAD//2


def draw(draw_info,sorting_algo_name,ascending,elapsed_time=0,peak_memory=0,cpu_percent=0):
	draw_info.window.fill(draw_info.BACKGROUD_COLOR)

	title = draw_info.FONT.render(f"{sorting_algo_name} - {'Ascending'if ascending else 'Descending'}",1,draw_info.RED)
	draw_info.window.blit(title,((draw_info.weidth/2 - title.get_width()/2),5)) 


	controles = draw_info.FONT.render(" R - Reset | SPACE - Start Sorting | A - Ascending | D - Decending",1,draw_info.BLACK)
	draw_info.window.blit(controles,((draw_info.weidth/2 - controles.get_width()/2),35)) # mid of screen


	sorting = draw_info.FONT.render("I - Insertion Sort | B - Bubble Sort | M - Merge Sort | Q - Quick Sort | H - Heap Sort",1,draw_info.BLACK)
	draw_info.window.blit(sorting,(draw_info.weidth/2 - sorting.get_width()/2,65))

	time_text = draw_info.FONT.render(
    f"Time: {elapsed_time:.4f} sec",
    True,
    draw_info.BLUE)
	draw_info.window.blit(time_text, (10, 10))

	memory_text = draw_info.FONT.render(
    f"Peak Mem: {peak_memory/1024:.1f} KB",
    True,
    draw_info.BLUE)
	draw_info.window.blit(memory_text, (10, 95))

	cpu_text = draw_info.FONT.render(
    f"CPU: {cpu_percent:.1f} %",
    True,
    draw_info.BLUE)
	draw_info.window.blit(cpu_text, (10, 120))

	draw_list(draw_info)
	pygame.display.update()



def draw_list(draw_info, color_positions={},clear_bg = False):# dictionary
	lst = draw_info.lst

	if clear_bg:
		clear_rect = (draw_info.SIDE_PAD//2,draw_info.TOP_PAD,
					draw_info.weidth-draw_info.SIDE_PAD,draw_info.heigth - draw_info.TOP_PAD)

		pygame.draw.rect(draw_info.window,draw_info.BACKGROUD_COLOR,clear_rect)


	for i , val in enumerate(lst):
		x = draw_info.start_x + i*draw_info.block_weidth
		y = draw_info.heigth - (val - draw_info.min_value)*draw_info.block_height

		color = draw_info.GRADIENTS[i%3]

		if i in color_positions:
			color = color_positions[i]

		pygame.draw.rect(draw_info.window,color,(x,y,draw_info.block_weidth,draw_info.heigth))


	if clear_bg:
		pygame.display.update()


def generate_strating_list(n,min_value,max_value):
	lst = []

	for _ in range(n):
		val = random.randint(min_value,max_value)
		lst.append(val)

	return lst

def bubble_sort(draw_info,ascending = True):

	lst = draw_info.lst


	for i in range(len(lst) - 1):
		for j in range(len(lst) - 1 - i):
			num1 = lst[j]
			num2 = lst[j+1]

			if (num2 < num1 and ascending) or (num2 > num1 and not ascending):
				lst[j],lst[j+1] = lst[j+1],lst[j]
				draw_list(draw_info,{j : draw_info.GREEN,j+1:draw_info.RED},True)
				yield True # importace

	return lst


def insertion_sort(draw_info,ascending=True):
	lst = draw_info.lst

	for i in range(1,len(lst)):
		current = lst[i]

		while True:
			ascending_sort = i>0 and lst[i-1] > current and ascending
			decending_sort = i>0 and lst[i-1] < current and not ascending

			if not ascending_sort and not decending_sort:
				break


			lst[i] = lst[i-1]
			i = i-1
			lst[i] = current
			draw_list(draw_info,{i-1:draw_info.GREEN,i:draw_info.RED},True)
			yield True


	return lst


def merge_sort(draw_info,ascending=True):
	lst = draw_info.lst

	yield from merge_sort_helper(draw_info,lst,0,len(lst)-1,ascending)

	return lst


def merge_sort_helper(draw_info,lst,left,right,ascending):
	if left >= right:
		return

	mid = (left + right)//2

	yield from merge_sort_helper(draw_info,lst,left,mid,ascending)
	yield from merge_sort_helper(draw_info,lst,mid+1,right,ascending)
	yield from merge(draw_info,lst,left,mid,right,ascending)


def merge(draw_info,lst,left,mid,right,ascending):
	left_half = lst[left:mid+1]
	right_half = lst[mid+1:right+1]

	i = j = 0
	k = left

	while i < len(left_half) and j < len(right_half):
		if (left_half[i] <= right_half[j] and ascending) or (left_half[i] >= right_half[j] and not ascending):
			lst[k] = left_half[i]
			i += 1
		else:
			lst[k] = right_half[j]
			j += 1

		draw_list(draw_info,{k:draw_info.GREEN},True)
		yield True
		k += 1

	while i < len(left_half):
		lst[k] = left_half[i]
		i += 1
		draw_list(draw_info,{k:draw_info.GREEN},True)
		yield True
		k += 1

	while j < len(right_half):
		lst[k] = right_half[j]
		j += 1
		draw_list(draw_info,{k:draw_info.GREEN},True)
		yield True
		k += 1


def quick_sort(draw_info,ascending=True):
	lst = draw_info.lst

	yield from quick_sort_helper(draw_info,lst,0,len(lst)-1,ascending)

	return lst


def quick_sort_helper(draw_info,lst,low,high,ascending):
	if low >= high:
		return

	pivot = lst[high]
	i = low - 1

	for j in range(low,high):
		if (lst[j] <= pivot and ascending) or (lst[j] >= pivot and not ascending):
			i += 1
			lst[i],lst[j] = lst[j],lst[i]
			draw_list(draw_info,{i:draw_info.GREEN,j:draw_info.RED,high:draw_info.RED},True)
			yield True

	lst[i+1],lst[high] = lst[high],lst[i+1]
	draw_list(draw_info,{i+1:draw_info.GREEN,high:draw_info.RED},True)
	yield True

	yield from quick_sort_helper(draw_info,lst,low,i,ascending)
	yield from quick_sort_helper(draw_info,lst,i+2,high,ascending)


def heap_sort(draw_info,ascending=True):
	lst = draw_info.lst
	n = len(lst)

	# build a max heap for ascending, min heap for descending
	for i in range(n//2 - 1,-1,-1):
		yield from sift_down(draw_info,lst,i,n,ascending)

	for end in range(n-1,0,-1):
		lst[0],lst[end] = lst[end],lst[0]
		draw_list(draw_info,{0:draw_info.GREEN,end:draw_info.RED},True)
		yield True
		yield from sift_down(draw_info,lst,0,end,ascending)

	return lst


def sift_down(draw_info,lst,root,size,ascending):
	while True:
		largest = root
		left = 2*root + 1
		right = 2*root + 2

		if left < size and ((lst[left] > lst[largest] and ascending) or (lst[left] < lst[largest] and not ascending)):
			largest = left

		if right < size and ((lst[right] > lst[largest] and ascending) or (lst[right] < lst[largest] and not ascending)):
			largest = right

		if largest == root:
			break

		lst[root],lst[largest] = lst[largest],lst[root]
		draw_list(draw_info,{root:draw_info.GREEN,largest:draw_info.RED},True)
		yield True
		root = largest


def main():

	run = True
	clock = pygame.time.Clock()
 
	n =150
	min_value = 0
	max_value = 100

	lst = generate_strating_list(n,min_value,max_value)
	draw_info = DrawInformation(1000,700,lst)
	sorting = False
	ascending = True

	sorting_algorithum = bubble_sort
	sorting_algo_name = "Bubble Sorting"
	sorting_algorithum_generator = None

	#timing part
	start_time = None
	elapsed_time = 0

	#memory and cpu part
	peak_memory = 0
	cpu_percent = 0
	process = psutil.Process()
	process.cpu_percent()  # first call always returns 0, prime it
	cpu_frame_counter = 0

	while run:

		clock.tick(160)

		if sorting:
			elapsed_time = time.perf_counter() - start_time
			peak_memory = tracemalloc.get_traced_memory()[1]
			try:
				next(sorting_algorithum_generator)
			except StopIteration:
				sorting = False
				elapsed_time = time.perf_counter() - start_time
				peak_memory = tracemalloc.get_traced_memory()[1]
				tracemalloc.stop()

		# cpu_percent measures since the last call, so sample every ~40 frames
		cpu_frame_counter += 1
		if cpu_frame_counter >= 40:
			cpu_percent = process.cpu_percent()
			cpu_frame_counter = 0

		draw(draw_info, sorting_algo_name, ascending, elapsed_time, peak_memory, cpu_percent)

		#pygame.display.update()
		#draw(draw_info)

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False

			if event.type != pygame.KEYDOWN:
				continue

			if event.key == pygame.K_r:
				lst = generate_strating_list(n,min_value,max_value)
				draw_info.set_list(lst)
				sorting = False
				if tracemalloc.is_tracing():
					tracemalloc.stop()
				elapsed_time = 0
				peak_memory = 0
			# elif event.key == pygame.K_SPACE and sorting == False:
			# 	sorting = True
			# 	sorting_algorithum_generator = sorting_algorithum(draw_info,ascending)
			elif event.key == pygame.K_SPACE and not sorting:
				sorting = True
				start_time = time.perf_counter()
				elapsed_time = 0
				peak_memory = 0
				if tracemalloc.is_tracing():
					tracemalloc.stop()
				tracemalloc.start()
				sorting_algorithum_generator = sorting_algorithum(draw_info,ascending)

			elif event.key == pygame.K_a and not sorting:
				ascending = True

			elif event.key == pygame.K_d and not sorting:
				ascending = False
			elif event.key == pygame.K_i and not sorting:
				sorting_algorithum = insertion_sort
				sorting_algo_name = "Insertion Sort"

			elif event.key == pygame.K_b and not sorting:
				sorting_algorithum = bubble_sort
				sorting_algo_name = "Bubble Sort"

			elif event.key == pygame.K_m and not sorting:
				sorting_algorithum = merge_sort
				sorting_algo_name = "Merge Sort"

			elif event.key == pygame.K_q and not sorting:
				sorting_algorithum = quick_sort
				sorting_algo_name = "Quick Sort"

			elif event.key == pygame.K_h and not sorting:
				sorting_algorithum = heap_sort
				sorting_algo_name = "Heap Sort"
		







	pygame.quit()


if __name__ == "__main__":
	main()