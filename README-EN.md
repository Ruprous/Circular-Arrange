# Circular Arrange v1.3.0 – for Blender 2.8.0 and above

**Circular Arrange** is a Blender add-on that lets you arrange multiple copies of a selected object in a circular pattern by specifying the number of instances and the radius.  
Install `circular_arrange.py` via *Edit > Preferences > Add-ons*, then enable it using the checkbox.

## How to Use

1. **Select the object** you want to duplicate and arrange in a circle, then press the `N` key to open the right-hand toolbar.
2. In the toolbar, find **"Circular Arrange"**.  
   Set your desired **Count** (number of instances) and **Radius**, then click the `Circular Arrange` button to apply.
3. Enable **Merge Objects** if you want to join all the arranged objects into a single one.
4. **Angle Mode** lets you control the rotation of each duplicated object:
    - **Relative**: Each object faces outward from the center of the circle.
        - **Relative Angle Offset (deg)**: Adds an additional rotation offset (in degrees) to each object in Relative mode.
    - **Fixed**: All objects are set to the same rotation angle.
        - **Fixed Angle (deg)**: Specifies the rotation angle (in degrees) for all objects in Fixed mode.

![Sample image](images/sampleimage01.png)
