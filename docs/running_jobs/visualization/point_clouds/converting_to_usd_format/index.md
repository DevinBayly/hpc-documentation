# Converting PCD point clouds to USD format for timeseries playback

This workflow allows you to combine a simulation, or lidar capture's output into a single universal scene descriptor file. This format is now supported by programs like blender which make it a feasible option for cinematic renders of scientific data with complex animation techniques. 

## Step 1: PCD file prep

If your data is in any other format, it's important to convert it to PCD. Typically the individual point cloud timestamps will be in `.ply` format, and this is a flexible format for including custom attributes for each point. It should be mentioned that when using python's `Open3d` program you may lose these custom attributes just by virtue of the way they implement the `pcd` file writer, so although it's tempting to just open a `ply` with this tool and export a `pcd` it's not suitable for general purpose data. Instead I advocate for starting from a `numpy array`.  

The pcd file format https://pointclouds.org/documentation/tutorials/pcd_file_format.html can be read about here, and in a pinch it's possible to write a custom `numpy array` to ascii `pcd` snippet. Here's an example for a point cloud with only one additional custom attribute field, but the example can be expanded on to include more

```
# Write PCD header
with open("your_pcd.pcd","w") as f:
    f.write(f"FIELDS x y z {field}\n")
    f.write("SIZE 4 4 4 4\n")
    f.write("TYPE F F F F\n")
    f.write("COUNT 1 1 1 1\n")
    f.write("WIDTH %d\n" % (numpy_array.shape[0]))
    f.write("HEIGHT 1\n")
    f.write("POINTS %d\n" % (numpy_array.shape[0]))
    f.write("DATA ascii\n")
    for i in range(numpy_array.shape[0]):
        f.write("{} {} {} {}\n".format(
            numpy_array[i, 0], numpy_array[i, 1],
            numpy_array[i, 2], numpy_array[i, 3]))
```

If you're working with `binary pcd` files instead of ascii it is possible to export an entire numpy array all at once, which may be more ideal if performance considerations are critical. **DESCRIPTION TBA**

## Step 2: Converting PCD files to USD

Configure your space as follows

* Put all the individual pcd files in a subfolder
* Add the [usd_creator.py](./scripts/usd_creator.py) script to your directory

Then load the docker/singularity container if you're not already in there, and run `python3 usd_creator.py <usd_output_file_name>`

This will search the current environment for any pcd files that can be found. For each one it will 
* parse the `pcd` header and convert it to `numpy` with the correct types for all the fields
* add it's point contents to a `USD` scene collection object using the index of the pcd file as a timestep value
* it will also add all the additional fields as `USD` attributes that 3d modeling programs can access later on



