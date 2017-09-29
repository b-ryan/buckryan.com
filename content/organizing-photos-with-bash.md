Title: Organizing photos with bash
Date: 2015-01-02
Category: Programming
Tags: bash
Author: Buck Ryan
Summary: Using bash tools to organize a random dump of photos

I've been trying to organize my photos recently. I hadn't kept up with them
and I recently discovered I have a pile of photos dumped into a single
directory. I like to separate photos by the day they were taken so I end up
with directories like:

```
2015-01-01_new-years-day
2014-12-31_new-years-eve
2014-12-25_christmas
...
```

Wanting to organize these as painlessly as I could think, I sought to run a few
bash commands to split my pile of photos into directories like these. The first
issue I ran into was the file formats - these were raw photos. I had found a
nice tool called `exif` (`sudo apt-get install exif`) which I could use to
extract the date the pictures were taken, but it only works on JPG images.

So step one was to convert the files. The
[ImageMagick](http://imagemagick.org/) tool (`sudo apt-get install
imagemagick`) has a command called `convert` that will do just that. To convert
them all without risking overwriting anything, a simple for loop works nicely:

```bash
for f in *.NEF; do
    convert $f $f.jpg
done
```

This will convert files like `DSC_0001.NEF` to `DSC_0001.NEF.jpg`. Running this
command was taking awhile and I wanted to see how much work was left to do.
`watch` is the perfect tool for the job. It lets you repeatedly run a command
and see its output. So all I needed to do was write a command that would list
all of the `.NEF` files that did not have corresponding `.NEF.jpg` files.  To
do that, I used:

```bash
for f in *.NEF; do
    ls $f.jpg &>/dev/null || echo $f
done
```

I ignored all output of `ls` (`&>/dev/null`) because the return code would be
enough to determine whether the file existed. More importantly, I didn't want
to have to parse through whatever output the command threw at me. The `|| echo
$f` will only be executed if the `ls` failed, indicating the file doesn't
exist.

I had issues running this directly with `watch`, but I didn't want to spend
time debugging. Instead I saved the command to a file and ran:

```bash
chmod +x script.sh
watch ./script.sh
```

Every 2 seconds the screen updated letting me know how many files were left
to convert.

While the conversion was running, I prepared to get exif data out of the jpg
files. I mentioned above that `exif` will do just that. Here's what a sample
run looked like:

```
  $ exif DSC_0093.JPG 
EXIF tags in 'DSC_0093.JPG' ('Motorola' byte order):
--------------------+----------------------------------------------------------
Tag                 |Value
--------------------+----------------------------------------------------------
Manufacturer        |
Model               |
X-Resolution        |500.0000000
Y-Resolution        |500.0000000
Resolution Unit     |Inch
Software            |Picasa 3.0
Date and Time       |2007:04:09 16:15:47
YCbCr Positioning   |Centered
Padding             |2060 bytes undefined data
Compression         |JPEG compression
X-Resolution        |72
Y-Resolution        |72
Resolution Unit     |Inch
Exif Version        |Exif Version 2.2
Date and Time (Origi|2007:12:25 11:07:52
Date and Time (Digit|2007:12:25 11:07:52
Components Configura|Y Cb Cr -
User Comment        |
Sub-second Time (Ori|00
Sub-second Time (Dig|00
FlashPixVersion     |FlashPix Version 1.0
Color Space         |Internal error (unknown value 65535)
Pixel X Dimension   |3008
Pixel Y Dimension   |2000
Custom Rendered     |Custom process
Image Unique ID     |517d7ada5c38d78cd60a3032343e64f1
Padding             |2060 bytes undefined data
Interoperability Ver|0100
--------------------+----------------------------------------------------------
EXIF data contains a thumbnail (5597 bytes).
```

(This was a *really* old photo - most of them were much more recent.)

I noticed there was the `Date and Time` tag in there. And in reading the man
page for `exif`, saw that I could ask for values of specific tags using the
`--tag` argument. Here is what happened for the same file above:

```
  $ exif --tag 'Date and Time' DSC_0093.JPG 
EXIF entry 'Date and Time' (0x132, 'DateTime') exists in IFD '0':
Tag: 0x132 ('DateTime')
  Format: 2 ('ASCII')
  Components: 20
  Size: 20
  Value: 2007:04:09 16:15:47
```

We can work with that! A few `grep` and `awk` commands later and I had:

```
  $ exif --tag 'Date and Time' DSC_0093.JPG \
    | grep Value \
    | awk '{print $2}' \
    | awk -F':' '{print $1 "-" $2 "-" $3}'
2007-04-09
```

To break that down: `grep Value` is pretty obvious. It will leave only the
line containing `Value` so now our result will look like

```
  Value: 2007:04:09 16:15:47
```

Then this gets piped to `awk '{print $2}'`. This is a very common type of awk
command to run. Since awk splits on whitespace by default, this will get us
the second column, which in this case contains the text

```
2007:04:09
```

I didn't care about the time of the photo since I'm planning to lump all of
the photos from the same day into a given directory. If I had wanted the date
*and* time, I could have used `awk '{print $2 " " $3}'`.

Now that I have the date, I want it in my preferred format of `yyyy-mm-dd` so
I once again turned to awk. This time I used `-F':'` to specify that I wanted
to split on `:` instead of whitespace. Then I rest of the command glues the
date, month, and year parts together with `-` in between.

So now I have to use all of this to make the directories and dump files into
them. Before actually creating any directories or moving any files, however,
I wanted to sanity check everything. I wrote a loop that spit out each of the
`*NEF.jpg` files and the date I calculated for them:

```bash
for f in *NEF.jpg; do
    echo -n "$f	"
    dt=$(exif --tag 'Date and Time' $f \
            | grep Value \
            | awk '{print $2}' \
            | awk -F':' '{print $1 "-" $2 "-" $3}')
    echo $dt
done
```

The `-n` flag to `echo` tells it to not print a newline. I then saved the
result of the command to calculate the picture's date to a variable called
`dt` so that I could reuse it in the code to follow. Here's a snippet of the
results:

```
DSC_1455.NEF.jpg	2014-07-28
DSC_1456.NEF.jpg	2014-07-28
DSC_1457.NEF.jpg	2014-07-28
DSC_1458.NEF.jpg	2014-07-28
DSC_1460.NEF.jpg	2014-07-28
DSC_1461.NEF.jpg	2014-07-28
DSC_1463.NEF.jpg	2014-07-28
DSC_1506.NEF.jpg	2014-09-03
DSC_1507.NEF.jpg	2014-09-03
DSC_1512.NEF.jpg	2014-09-03
```

After sanity checking the results, I felt confident enough to go forward. Here
is the final product:

```bash
for f in *NEF.jpg; do
    dt=$(exif --tag 'Date and Time' $f \
            | grep Value \
            | awk '{print $2}' \
            | awk -F':' '{print $1 "-" $2 "-" $3}')

    mkdir $dt &>/dev/null
    mv ${f%.jpg} $dt/
done
```

The most interesting part of this code is the `${f%.jpg}`. This chops `.jpg`
off of the end of the string. To fully grasp what's going on, check out [this
article](http://tldp.org/LDP/abs/html/string-manipulation.html), specifically
the section titled **Substring Removal**.

And that was it! Was a lot of faster than doing it by hand. Maybe there are
tools out there that could have done this for me, but I found this more fun.
You can really do some neat stuff with everyday command-line tools. I highly
recommend using them for tasks like this to become comfortable writing bash.
