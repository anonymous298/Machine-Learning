# %matplotlib inline
 
import matplotlib.pyplot as plt
 
#creating list of Month and Share_buy for Plotting Line graph
Month = ['January', 'February','March']
Share_buy = [10, 17, 30]
 
#plotting line plot
plt.title("Share's Buy in a month")
plt.plot(Month, Share_buy)