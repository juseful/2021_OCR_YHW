```
├── medicine
│   ├── annotations(50개)
│   │    ├──*.json
│   ├── images(143개)
│   │    ├── *.jpg or *.jpeg
```

```
├── jsonfile
│   ├── Identifier 
│   ├── name
│   ├── src_path
│   ├── label_path
│   ├── category
│   ├── type
│   ├── images
│   │    ├── image 1
│   │    │   ├── identifier
│   │    │   ├── name
│   │    │   ├── type
│   │    │   ├── width
│   │    │   ├── height
│   │    │   ├── data_captured
│   │    │   ├── shutter_speed
│   │    │   ├── f_stop
│   │    │   ├── gps
│   │    │   ├── age
│   │    │   ├── gender
│   │    │   ├── writer_num
│   │    │   ├── shooting_env
│   │    │   ├── dust
│   │    │   ├── class
│   │    │   ├── product_name
│   │    │   ├── product_category
│   │    ├── image 2
│   │    │   ├── identifier
│   │    │   ├──......
│   ├── annotations
│   │    ├── annotation 1
│   │    │   ├── polygons
│   │    │   │   ├── polygon 1
│   │    │   │   │   ├── id
│   │    │   │   │   ├── type
│   │    │   │   │   ├── text
│   │    │   │   │   ├── points
│   │    │   │   ├── polygon 2
│   │    │   │   │   ├── ......
│   │    │   ├── bbox
│   │    │   │   ├── bbox 1
│   │    │   │   │   ├── id
│   │    │   │   │   ├── x
│   │    │   │   │   ├── y
│   │    │   │   │   ├── width
│   │    │   │   │   ├── height
│   │    │   │   ├── bbox 2
│   │    │   │   │   ├── ......

```