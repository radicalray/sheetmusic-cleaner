### Sheet Music Cleaner

Uses openCV to clean the background of sheet music

### Dependencies

```
opencv (good luck)
ImageMagick (brew install imagemagick + brew install ghostscript for pdf support)
numpy
```

### How to run

Break pdf into photos using ImageMagick by:

```
convert -density 300 "./sheetmusic.pdf" music.png
```

Add images to musicsheet folder then run

```
python threshold.py
```

