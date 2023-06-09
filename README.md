# happy-tools
Python tools for dealing with hyper-spectral images.

## Installation

```
pip install git+https://github.com/wairas/happy-tools.git
```

## Command-line

### HSI to CSV

```
usage: happy-hsi2csv [-h] -d DIR -m DIR -s FILE -o DIR
                     [-M [METADATA_VALUES [METADATA_VALUES ...]]] -T
                     TARGETS [TARGETS ...]

Generates CSV files from hyper-spectral images.

optional arguments:
  -h, --help            show this help message and exit
  -d DIR, --data_dir DIR
                        the directory with the hyper-spectral data files
                        (default: None)
  -m DIR, --metadata_dir DIR
                        the directory with the meta-data JSON files (default:
                        None)
  -s FILE, --sample_ids FILE
                        the JSON file with the array of sample IDs to process
                        (default: None)
  -o DIR, --output_dir DIR
                        the directory to store the results in (default: None)
  -M [METADATA_VALUES [METADATA_VALUES ...]], --metadata_values [METADATA_VALUES [METADATA_VALUES ...]]
                        the meta-data values to add to the output (default:
                        None)
  -T TARGETS [TARGETS ...], --targets TARGETS [TARGETS ...]
                        the target values to generate data for (default: None)
```

### HSI to RGB

```
usage: happy-hsi2rgb [-h] -i INPUT_DIR [INPUT_DIR ...] [-r] [-e EXTENSION]
                     [-b BLACK_REFERENCE] [-w WHITE_REFERENCE] [-a]
                     [--red INT] [--green INT] [--blue INT] [-o OUTPUT_DIR]
                     [--width INT] [--height INT] [-n] [-v]

Fake RGB image generator for HSI files.

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT_DIR [INPUT_DIR ...], --input_dir INPUT_DIR [INPUT_DIR ...]
                        Path to the scan file (ENVI format) (default: None)
  -r, --recursive       whether to traverse the directories recursively
                        (default: False)
  -e EXTENSION, --extension EXTENSION
                        The file extension to look for (default: .hdr)
  -b BLACK_REFERENCE, --black_reference BLACK_REFERENCE
                        Path to the black reference file (ENVI format)
                        (default: None)
  -w WHITE_REFERENCE, --white_reference WHITE_REFERENCE
                        Path to the white reference file (ENVI format)
                        (default: None)
  -a, --autodetect_channels
                        whether to determine the channels from the meta-data
                        (overrides the manually specified channels) (default:
                        False)
  --red INT             the wave length to use for the red channel (0-based)
                        (default: 0)
  --green INT           the wave length to use for the green channel (0-based)
                        (default: 0)
  --blue INT            the wave length to use for the blue channel (0-based)
                        (default: 0)
  -o OUTPUT_DIR, --output_dir OUTPUT_DIR
                        The directory to store the fake RGB PNG images instead
                        of alongside the HSI images. (default: None)
  --width INT           the width to scale the images to (<= 0 uses image
                        dimension) (default: 0)
  --height INT          the height to scale the images to (<= 0 uses image
                        dimension) (default: 0)
  -n, --dry_run         whether to omit saving the PNG images (default: False)
  -v, --verbose         whether to be more verbose with the output (default:
                        False)
```


### ENVI Viewer

```
usage: happy-viewer [-h] [-s SCAN] [-f BLACK_REFERENCE] [-w WHITE_REFERENCE]
                    [-r INT] [-g INT] [-b INT] [--autodetect_channels]
                    [--usage: happy-hsi2rgb [-h] -i INPUT_DIR [INPUT_DIR ...] [-r] [-e EXTENSION]
                     [-b BLACK_REFERENCE] [-w WHITE_REFERENCE] [-a]
                     [--red INT] [--green INT] [--blue INT] [-o OUTPUT_DIR]
                     [--width INT] [--height INT] [-n] [-v]

Fake RGB image generator for HSI files.

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT_DIR [INPUT_DIR ...], --input_dir INPUT_DIR [INPUT_DIR ...]
                        Path to the scan file (ENVI format) (default: None)
  -r, --recursive       whether to traverse the directories recursively
                        (default: False)
  -e EXTENSION, --extension EXTENSION
                        The file extension to look for (default: .hdr)
  -b BLACK_REFERENCE, --black_reference BLACK_REFERENCE
                        Path to the black reference file (ENVI format)
                        (default: None)
  -w WHITE_REFERENCE, --white_reference WHITE_REFERENCE
                        Path to the white reference file (ENVI format)
                        (default: None)
  -a, --autodetect_channels
                        whether to determine the channels from the meta-data
                        (overrides the manually specified channels) (default:
                        False)
  --red INT             the wave length to use for the red channel (0-based)
                        (default: 0)
  --green INT           the wave length to use for the green channel (0-based)
                        (default: 0)
  --blue INT            the wave length to use for the blue channel (0-based)
                        (default: 0)
  -o OUTPUT_DIR, --output_dir OUTPUT_DIR
                        The directory to store the fake RGB PNG images instead
                        of alongside the HSI images. (default: None)
  --width INT           the width to scale the images to (<= 0 uses image
                        dimension) (default: 0)
  --height INT          the height to scale the images to (<= 0 uses image
                        dimension) (default: 0)
  -n, --dry_run         whether to omit saving the PNG images (default: False)
  -v, --verbose         whether to be more verbose with the output (default:
                        False)
keep_aspectratio] [--annotation_color HEXCOLOR]
                    [--redis_host HOST] [--redis_port PORT]
                    [--redis_pw PASSWORD] [--redis_in CHANNEL]
                    [--redis_out CHANNEL] [--redis_connect]
                    [--sam_marker_size INT] [--sam_marker_color HEXCOLOR]
                    [--sam_min_obj_size INT]

ENVI Hyper-spectral Image Viewer. Offers contour detection using SAM (Segment-
Anything: https://github.com/waikato-datamining/pytorch/tree/master/segment-
anything)

optional arguments:
  -h, --help            show this help message and exit
  -s SCAN, --scan SCAN  Path to the scan file (ENVI format) (default: None)
  -f BLACK_REFERENCE, --black_reference BLACK_REFERENCE
                        Path to the black reference file (ENVI format)
                        (default: None)
  -w WHITE_REFERENCE, --white_reference WHITE_REFERENCE
                        Path to the white reference file (ENVI format)
                        (default: None)
  -r INT, --red INT     the wave length to use for the red channel (default:
                        0)
  -g INT, --green INT   the wave length to use for the green channel (default:
                        0)
  -b INT, --blue INT    the wave length to use for the blue channel (default:
                        0)
  --autodetect_channels
                        whether to determine the channels from the meta-data
                        (overrides the manually specified channels) (default:
                        False)
  --keep_aspectratio    whether to keep the aspect ratio (default: False)
  --annotation_color HEXCOLOR
                        the color to use for the annotations like contours
                        (hex color) (default: #ff0000)
  --redis_host HOST     The Redis host to connect to (IP or hostname)
                        (default: localhost)
  --redis_port PORT     The port the Redis server is listening on (default:
                        6379)
  --redis_pw PASSWORD   The password to use with the Redis server (default:
                        None)
  --redis_in CHANNEL    The channel that SAM is receiving images on (default:
                        sam_in)
  --redis_out CHANNEL   The channel that SAM is broadcasting the detections on
                        (default: sam_out)
  --redis_connect       whether to immediately connect to the Redis host
                        (default: False)
  --sam_marker_size INT
                        The size in pixels for the SAM points (default: 7)
  --sam_marker_color HEXCOLOR
                        the color to use for the SAM points (hex color)
                        (default: #ff0000)
  --sam_min_obj_size INT
                        The minimum size that SAM contours need to have (<= 0
                        for no minimum) (default: -1)
```
