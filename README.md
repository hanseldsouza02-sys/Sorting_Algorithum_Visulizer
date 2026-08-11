# Sorting_Algorithm_Visualizer

A Python + Pygame desktop application that visualizes how popular sorting algorithms work, step by step. Numbers are drawn as vertical bars, and as an algorithm runs you can watch the bars swap and settle into order in real time. It also displays live performance metrics (execution time, peak memory, and CPU usage) so you can compare how the algorithms behave.

Features:
- 5 sorting algorithms: Bubble, Insertion, Merge, Quick, and Heap Sort
- Ascending or descending sort order
- Color-coded animation — bars being compared/swapped are highlighted (green / red) while sorting
- Live performance stats on screen:
- Elapsed time 
- Peak memory usage 
- CPU usage percentage 
- Generate a fresh random list at any time to re-run

Controls:
Space : Start sorting
R     :  Reset with a new random list
A     :  Ascending order
D     :  Descending order
B     :  Bubble Sort
I     :  Insertion Sort
M     :  Merge Sort
Q     :  Quick Sort
H     :  Heap Sort


Tech Stack:
- Python 3
- Pygame — window rendering and animation
- psutil — CPU usage monitoring
- tracemalloc & time — memory and timing measurement (standard library)

How It Works:
Each sorting function is written as a Python generator that yields after every comparison/swap. The main loop advances the generator one step per frame and redraws the bars, producing the smooth animation. When the algorithm finishes, the final time and peak memory are locked in and displayed.


Algorithm Complexity Reference:

<img width="1756" height="640" alt="image" src="https://github.com/user-attachments/assets/5ec11f98-c08d-4295-bf14-e3f366ea50d7" />



