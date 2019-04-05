# Introduction
  
  TIoU-metric maybe more effective in evaluating curve text since IoU 0.5 for curved text could be visually unaccetable.
  
## Evaluation on SCUT-CTW1500
det_ctw1500.zip is an example detection results from [SCUT-CTW1500](https://github.com/Yuliang-Liu/Curve-Text-Detector/tree/master/tools/ctw1500_evaluation). 
ctw1500-gt.zip is the gt of test set  from [SCUT-CTW1500](https://github.com/Yuliang-Liu/Curve-Text-Detector).

Run
  ```shell
  python script.py -g=ctw1500-gt.zip -s=det_ctw1500.zip
```
will produce 

```
('num_gt, num_det: ', 3068, 3340) 

Origin:

('recall: ', 0.8162, 'precision: ', 0.7497, 'hmean: ', 0.7815)

TIoU-metric:

('tiouRecall:', 0.52, 'tiouPrecision:', 0.572, 'tiouHmean:', 0.545)
```

The result is exactly the same as the official implement of [SCUT-CTW1500](https://github.com/Yuliang-Liu/Curve-Text-Detector/tree/master/tools/ctw1500_evaluation).

The ccw-sortdet.py might be helpful to transfer your result into valid format.

## Evaluation on Total-Text
total-text_baseline.zip in an example from the author of [Total-Text](https://github.com/cs-chan/Total-Text-Dataset).

total-text-gt.zip is the gt of test set from [Total-Text](https://github.com/cs-chan/Total-Text-Dataset).

Run
  ```shell
  python script.py -g=total-text-gt.zip -s=total-text_baseline.zip
```
will produce

```
('num_gt, num_det: ', 2214, 2098)
Origin:
('recall: ', 0.7014, 'precision: ', 0.8038, 'hmean: ', 0.7492)
TIoU-metric:
('tiouRecall:', 0.479, 'tiouPrecision:', 0.619, 'tiouHmean:', 0.54)
```

Note each line of each file of detection is following x,y,...,x,y.. format. (Official Total-text requires y,x,y,x,...)
