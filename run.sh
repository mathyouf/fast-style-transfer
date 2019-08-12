mkdir tests

export PYTHONUNBUFFERED=0
python style.py --style examples/style/tsai1.jpg \
  --checkpoint-dir /artifacts \
  --vgg-path /styletransfer/data/imagenet-vgg-verydeep-19.mat \
  --train-path /datasets/coco/coco_train2014 \
  --test examples/content/face.jpg \
  --test-dir tests/ \
  --content-weight 1.5e1 \
  --checkpoint-iterations 1000 \
  --batch-size 69

python evaluate.py --checkpoint /artifacts \
--in-path examples/content \
--out-path /artifacts --allow-different-dimensions
