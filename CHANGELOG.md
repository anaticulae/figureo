# changelog

Every noteable change is logged here.

## v0.17.3

### Fix

* skip very small items (889d0e5ada1c)

### Documentation

* adjust modules path (d550973fe8a0)

## v0.17.2

### Feature

* make error rate content length decedent (2a87d051f19e)

## v0.17.1

### Fix

* merge more little chars to a single line (ee8a2efaaff8)

## v0.17.0

### Feature

* add support for rotated pages (4296ee15a1b0)

### Fix

* do not skip line rectangles (07a79cea548e)
* hack utila workstep input path computation (7d0d3c34a254)

### Documentation

* Happy New Year! (725c5f0cad44)

## v0.16.0

### Feature

* improve last line check (2327e4c02b28)

### Fix

* merge text figures into second try (ecb8d1f264f4)
* merge images only into text figures (89c0541032e7)

## v0.15.0

### Feature

* skip formula bounding as valid figureo area (289390a65520)

### Fix

* reduce start of line to reduce fail detection (4e5fa2dc53a2)
* skip invisible item (df6874d52a6d)

## v0.14.0

### Feature

* skip first text line included into figure (acc37553f690)

## v0.13.0

### Feature

* check for non extracted text figures (207f6edcc74a)
* create figure data if required (628acea763ce)

## v0.12.0

### Feature

* skip figures with too many invalid figures (65318b55b75e)
* skip hidden rectangles (8ee8991bd23a)
* make LTRectangle index able (e59bfb11f43a)

### Fix

* support figure inside figure (329820439d9c)
* shrink bad printed figure bounding (4ae85775a6a4)

## v0.11.0

### Feature

* use captions to divide cluster areas (cf2d9122a514)

### Fix

* reduce tolerance to improve figure detection (70c80840b1f6)

### Documentation

* update outdated comment (877a4f80e6be)

## v0.10.3

### Feature

* add figure flag (e4e57af53207)

## v0.10.2

### Fix

* hidden flag scrambled the path, use improved loader (fd8dbb4944b6)

## v0.10.1

### Fix

* run standard before cleanup (b4c413f905d0)
* do not try to load pdf as images (bf41285e6284)

## v0.10.0

### Feature

* add cleanup step to disable images which are part of figure (2226ce224d21)

## v0.9.0

### Feature

* adjust figure extractor to detect text inline images (10ed188b91e1)
* increase valid area to detect bad renderer images (cdd54f4388a8)

## v0.8.1

### Feature

* make figure extractor more precise (c40ef5ee2034)

## v0.8.0

### Feature

* add basic cli infrastructure (57260d79879e)
* skip image only figures (3d8fd3f22ef2)

## v0.7.0

### Feature

* skip content with to many dots (500596b6023f)

### Fix

* skip empty text items (ff99984f149a)
* skip dots as potential figure content (f08c820f67bc)
* table checker was not used and return wrong result (a42bb74aeea5)

## v0.6.0

### Feature

* add debugging information (ea04afc17a78)
* use extracted table to improve figure detector (3405439c96af)

## v0.5.0

### Feature

* reduce verbosity of logging (22f4b45e9f2a)
* increase valid figure text item (f850c9aa52d0)
* add some space to bounding (f00edba1486d)
* skip caption line to improve extraction result (2a32d788a5b0)

## v0.4.0

### Feature

* crop figures from pdf extraction (29b7f56eb483)

### Fix

* use default bounding for white pages (a5bcfeeaed90)

## v0.3.0

### Feature

* rename output to write to rawmaker__images folder (674c3476a8eb)

## v0.2.0

### Feature

* use content border as valid figure content (88607fa94971)
* add groupme content to shrink figure extraction (954891a3be5e)

## v0.1.0

### Feature

* move code from rawmaker (a33bde8a369a)

## v0.0.0 Initial release
