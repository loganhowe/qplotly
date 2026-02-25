"""Visual demonstration comparing legend styles."""
import sys
sys.path.insert(0, r'C:\cqc\qplotly')

import qplotly
import numpy as np

print("Creating legend comparison demonstration...\n")

x = np.linspace(0, 10, 100)

# Create a comparison figure
fig, axes = qplotly.subplots(2, 2, figsize=(14, 10),
                              subplot_titles=['Default (upper right, opaque)',
                                            'Upper left',
                                            'Center (semi-transparent)',
                                            'Lower right, no frame'])

# Default
axes[0][0].plot(x, np.sin(x), label='sin(x)')
axes[0][0].plot(x, np.cos(x), label='cos(x)')
axes[0][0].plot(x, np.sin(2*x) * 0.5, label='0.5*sin(2x)')
axes[0][0].legend()  # Default: upper right, opaque
axes[0][0].grid(True)
axes[0][0].title('Default')

# Upper left
axes[0][1].plot(x, np.sin(x), label='sin(x)')
axes[0][1].plot(x, np.cos(x), label='cos(x)')
axes[0][1].plot(x, np.sin(2*x) * 0.5, label='0.5*sin(2x)')
axes[0][1].legend(loc='upper left')
axes[0][1].grid(True)
axes[0][1].title('Upper Left')

# Center, semi-transparent
axes[1][0].plot(x, np.sin(x), label='sin(x)')
axes[1][0].plot(x, np.cos(x), label='cos(x)')
axes[1][0].plot(x, np.sin(2*x) * 0.5, label='0.5*sin(2x)')
axes[1][0].legend(loc='center', framealpha=0.5)
axes[1][0].grid(True)
axes[1][0].title('Center, 50% Transparent')

# Lower right, no frame
axes[1][1].plot(x, np.sin(x), label='sin(x)')
axes[1][1].plot(x, np.cos(x), label='cos(x)')
axes[1][1].plot(x, np.sin(2*x) * 0.5, label='0.5*sin(2x)')
axes[1][1].legend(loc='lower right', frameon=False)
axes[1][1].grid(True)
axes[1][1].title('Lower Right, No Frame')

fig.suptitle('Legend Positioning and Styling - All Inside Plot Boundaries', fontsize=14)
fig.savefig(r'C:\cqc\qplotly\colormap_debugging\legend_comparison_demo.png',
            width=1400, height=1000)

print("Saved: legend_comparison_demo.png")
print("\nAll legends are positioned inside the plot boundaries!")
print("Notice:")
print("  - Upper right is the default position")
print("  - All positions have proper margins from edges")
print("  - Backgrounds are opaque by default (except when framealpha set)")
print("  - Black borders by default (unless frameon=False)")
