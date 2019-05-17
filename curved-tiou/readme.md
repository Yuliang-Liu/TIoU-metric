# Introduction
  
  TIoU-metric maybe more effective in evaluating curved text since IoU 0.5 for curved text could be visually unaccetable.
  
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

***The ccw-sortdet.py might be helpful to transfer your result into valid format.***

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

## State-of-the-art Results on Total-Text and CTW1500 (TIoU)
We sincerely appreciate the authors of recent and previous state-of-the-art methods for providing their results for evaluating TIoU metric in curved text benchmarks. The results are listed below:

### Total-Text

| Methods on Total-Text     |  TIoU-Recall (%)  |  TIoU-Precision (%)  |   TIoU-Hmean (%)     |    Publication   | 
|:--------:  | :-----:   | :----:      |  :-----:     | :-----: |
|LSN+CC [[paper]](https://arxiv.org/abs/1903.09837)| 48.4     |  59.8       |    53.5      |   arXiv 1903 |
|Total-text-baseline [[paper]](https://github.com/cs-chan/Total-Text-Dataset)|  47.9    |  61.9    |    54.0      |   - |
|CRAFT [[paper]](https://arxiv.org/abs/1904.01941) | 54.1 | 65.5 | 59.3 | CVPR 2019 |
|CTD+TLOC [[paper]](https://arxiv.org/abs/1712.02170)[[code]](https://github.com/Yuliang-Liu/Curve-Text-Detector) | 50.8     |  62.0       |    55.8      |   arXiv 1712 | 
|PSENet [[paper]](https://arxiv.org/abs/1903.12473)[[code]](https://github.com/whai362/PSENet)  | 53.3 |  66.9      |    59.3     |  CVPR 2019 |
|TextField [[paper]](https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=8648420)|  58.0    |  63.0    |    60.4      |   TIP 2019 |
|Mask TextSpotter [[paper]](https://arxiv.org/abs/1807.02242)|  54.5    |  68.0    |    60.5      |   ECCV 2018 |
|CRAFT [[paper]](https://arxiv.org/abs/1904.01941) | 54.1 | 65.5 | 59.3 | CVPR 2019 |
|SPCNet [[paper]](https://arxiv.org/abs/1811.08605) | 61.8     |  69.4       |    65.4      |   AAAI 2019 | 

### CTW1500

| Methods on CTW1500     |  TIoU-Recall (%)  |  TIoU-Precision (%)  |   TIoU-Hmean (%)     |    Publication   | 
|:--------:  | :-----:   | :----:      |  :-----:     | :-----: |
|CTD+TLOC [[paper]](https://arxiv.org/abs/1712.02170)[[code]](https://github.com/Yuliang-Liu/Curve-Text-Detector) | 42.5     |  53.9       |    47.5      |   arXiv 1712 | 
|LSN+CC [[paper]](https://arxiv.org/abs/1903.09837)| 55.9     |  64.8       |    60.0      |   arXiv 1903 |
|PSENet [[paper]](https://arxiv.org/abs/1903.12473)[[code]](https://github.com/whai362/PSENet)  | 54.9 |  67.6      |    60.6     |  CVPR 2019 |
|CRAFT [[paper]](https://arxiv.org/abs/1904.01941) | 56.4 | 66.3 | 61.0 | CVPR 2019 |
|MSR [[paper]](https://arxiv.org/abs/1901.02596)|  56.3    |  67.3     |    61.3    |   arXiv 1901 |
|TextField [[paper]](https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=8648420)|  57.2    |  66.2    |    61.4      |   TIP 2019 | 
|TextMountain [[paper]](https://arxiv.org/pdf/1811.12786.pdf)  | 59.2   |  66.9       |    62.7     |  arXiv 1811 |
|PAN Mask R-CNN [[paper]](https://arxiv.org/pdf/1811.09058.pdf)| 61.0    |  70.0       |    65.2     |  WACV 2019 |
