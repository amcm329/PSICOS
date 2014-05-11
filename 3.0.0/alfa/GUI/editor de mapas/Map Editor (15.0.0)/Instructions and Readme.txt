Map Editor v.15.0.0
Ian Mallett

ABOUT:
	Map Editor was rewritten basically from scratch for version 15.0.0, because the previous version was horrible.  This version uses a vertex shader to displace a heightmap.  Consequently, all computation happens on the very fast GPU.  I can edit 1024x1024 maps in realtime, and probably beyond, though I have not tested.  It is released under the terms described on my website "geometrian.com" under "Projects" or "About".
	
	The generated heightmap might look a little strange.  Greyscale heightmaps can only store 256 different heights.  This leads to the landscape being choppy-looking.  To fix this, the generated heightmap stores extra information in the green and blue channels.  To reconstruct the correct height, use the following:
		height = red/255.0 + green/(255.0*255.0) + blue/(255.0*255.0*255.0)
	
	This allows for extremely precise heightmaps with almost the same precision as a standard float (in C).  It is also backwards-compatible with normal heightmaps in that the red channel (which is what is typically sampled in a greyscale heightmap) is actually a standard heightmap!
	
	The resolution is currently hardcoded around line 15 in "Map Editor.py".  Change it as you will.

VERSIONS:
	Version 15.0.0 is a complete rewrite.  Not everything is implemented, but it's orders of magnitude better than the previous versions.  It's much faster, a lot cleaner, and more capable in most ways.

TO RUN:
	Click on "Map Editor.py".

CONTROLS:
	--Left click applies the current tool
	--Scrollwheel changes the tool's size
	
	--Buttons at top left change the current tool
	--Buttons at bottom save to or load from "test.png"
	--Buttons at top right change the rendering mode
	
	--Holding CTRL while left clicking and dragging rotates the camera
	--Holding CTRL while moving the scrollwheel zooms the camera
	
	--R resets the camera to the view it started with
	--ESCAPE or the "X" exits without saving
	
TODO:
	--Selection of grid size
	--Faster map generation (the bottleneck is generating a display list; if this were done as a VBO with NumPy, it could be done much faster--although it should be noted that I have already gone out of my way to not make NumPy an extra dependency (especially since it's hard to find a legit version for Python 3.3).
	--Faster saving (the only way this would really work is through GPU acceleration)
	
	--Holding CTRL while right clicking and dragging translates the camera
	--Save/load dialogs (make wxWidgets dependency optional, I think)
	--Changing the tool size without the scrollwheel
	--Zoom without scrollwheel
	--Tool/key to reset camera
	--Customizable controls?
	--More tools (e.g., erode, smooth, sharpen, etc.)
	
	--Viewing a diffuse texture (basically: change the texture you see)
	--Multiple diffuse textures/full texture mapping?
	--Hierarchical grid so that high resolution maps can still be edited nicely on a macro level
	--Visualize the heightmap while editing?
	--Lighting?
	
	--A viewer for the generated heightmap
	
	--Alpha channel for additional precision?  Basically unnecessary, methinks.

	--Fix bugs
	
KNOWN BUGS:
	--Pathological placement of the camera can cause GLU to crash the program with a failed projection error.
	--Occasionally, error messages relating to objects not being fully deleted before the OpenGL context ends are printed to the console before the program exits.  These have just about no effect practically, but are annoying to me personally.