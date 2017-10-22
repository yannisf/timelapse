# Timelapse

## Content acquisition

First obtain the initial images. You might want to crop them to keep for instance just a specific part. The same cropping should be applied to all images. After the cropping all images will be of the same size using the same point of view.

```
sample center cropping command using Imagemagick's convert
```

## Zooming

To emulate a zoom effect from the center out, you should crop them using a variable geometry for each image. So to perfom a zoom out effect you should crop the first image to the intented video resolution and gradually increase the cropped image to the initial image resolution. The formula is like so:

```python
x_coefficient = (x_original - x_final) / num_of_images
y_coefficient = (y_original - y_final) / num_of_images

x_size(i) = x_original + x_coefficient * i
y_size(i) = y_original + y_coefficient * i
```

where _i_, the image sequence number that falls in the range _[0, num_of_images]_

After this cropping, you will find yourself with images of different size. Resize all of them to the intended video resolution.

## Create the video

To create the video ffmpeg is used. The sample command is:

```shell
> avconv -r 10 -framerate 30 -i 'R_%05d.JPG' out.mkv
```

- **-r 10**: Show 10 images per second
- **-framerate 30**: Show 30 frames per second
- **-i '%05d.JPG'**: The file pattern

So, with _10 images per second_, which means _0.1 seconds per image_, for a total of _120 images_,  a video of _12 seconds_ is produced (120 images / 10 images per second = 12 seconds). If originally you were shooting _every 10 seconds_, and captured _120 images_, which means you captured `120 * 10 = 1200sec (or 20min)` of actual  activity, the timelapse will have compressed _20 minutes_ to _12 seconds_.


## Add audio to video

```
avconv -i ../../audio/audio.mp3 -i out.mkv -c copy video.mkv
```
