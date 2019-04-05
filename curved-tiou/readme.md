# Introduction
  
  TIoU-metric maybe more effective in evaluating curve text since IoU 0.5 for curved text could be visually unaccetable.
  
# Getting Started

## Evaluating on SCUT-CTW1500
det_ctw1500.zip is an example from [SCUT-CTW1500](https://github.com/Yuliang-Liu/Curve-Text-Detector/tree/master/tools/ctw1500_evaluation) example results. 
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
