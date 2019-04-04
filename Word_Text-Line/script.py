#!/usr/bin/env python
# -*- coding: utf-8 -*-
from collections import namedtuple
import rrc_evaluation_funcs
import importlib

import math 

def evaluation_imports():
    """
    evaluation_imports: Dictionary ( key = module name , value = alias  )  with python modules used in the evaluation. 
    """    
    return {
            'Polygon':'plg',
            'numpy':'np'
            }

def default_evaluation_params():
    """
    default_evaluation_params: Default parameters to use for the validation and evaluation.
    """
    return {
                'IOU_CONSTRAINT' :0.5,
                'AREA_PRECISION_CONSTRAINT' :0.5,
                'GT_SAMPLE_NAME_2_ID':'gt_img_([0-9]+).txt',
                'DET_SAMPLE_NAME_2_ID':'res_img_([0-9]+).txt',
                'LTRB':False, #LTRB:2points(left,top,right,bottom) or 4 points(x1,y1,x2,y2,x3,y3,x4,y4)
                'CRLF':False, # Lines are delimited by Windows CRLF format
                'CONFIDENCES':False, #Detections must include confidence value. AP will be calculated
                'PER_SAMPLE_RESULTS':True #Generate per sample results and produce data for visualization
            }

def validate_data(gtFilePath, submFilePath, gtTextLineFilePath, evaluationParams):
    """
    Method validate_data: validates that all files in the results folder are correct (have the correct name contents).
                            Validates also that there are no missing files in the folder.
                            If some error detected, the method raises the error
    """
    gt = rrc_evaluation_funcs.load_zip_file(gtFilePath,evaluationParams['GT_SAMPLE_NAME_2_ID'])

    subm = rrc_evaluation_funcs.load_zip_file(submFilePath,evaluationParams['DET_SAMPLE_NAME_2_ID'],True)

    gt_tl = rrc_evaluation_funcs.load_zip_file(gtTextLineFilePath,evaluationParams['GT_SAMPLE_NAME_2_ID'])
    
    #Validate format of GroundTruth
    print('validating gt ...')
    for k in gt:
        rrc_evaluation_funcs.validate_lines_in_file(k,gt[k],evaluationParams['CRLF'],evaluationParams['LTRB'],True)
    print('validating gt textline ...')
    for k in gt_tl:
        rrc_evaluation_funcs.validate_lines_in_file(k,gt_tl[k],evaluationParams['CRLF'],evaluationParams['LTRB'],True)

    #Validate format of results
    print('validating detection ...')
    for k in subm:
        if (k in gt) == False :
            raise Exception("The sample %s not present in GT" %k)
        
        rrc_evaluation_funcs.validate_lines_in_file(k,subm[k],evaluationParams['CRLF'],evaluationParams['LTRB'],False,evaluationParams['CONFIDENCES'])


    
def evaluate_method(gtFilePath, submFilePath, gtTextLineFilePath, evaluationParams):
    """
    Method evaluate_method: evaluate method and returns the results
        Results. Dictionary with the following values:
        - method (required)  Global method metrics. Ex: { 'Precision':0.8,'Recall':0.9 }
        - samples (optional) Per sample metrics. Ex: {'sample1' : { 'Precision':0.8,'Recall':0.9 } , 'sample2' : { 'Precision':0.8,'Recall':0.9 }
    """    
    for module,alias in evaluation_imports().iteritems():
        globals()[alias] = importlib.import_module(module)    
    
    def polygon_from_points(points):
        """
        Returns a Polygon object to use with the Polygon2 class from a list of 8 points: x1,y1,x2,y2,x3,y3,x4,y4
        """        
        resBoxes=np.empty([1,8],dtype='int32')
        resBoxes[0,0]=int(points[0])
        resBoxes[0,4]=int(points[1])
        resBoxes[0,1]=int(points[2])
        resBoxes[0,5]=int(points[3])
        resBoxes[0,2]=int(points[4])
        resBoxes[0,6]=int(points[5])
        resBoxes[0,3]=int(points[6])
        resBoxes[0,7]=int(points[7])
        pointMat = resBoxes[0].reshape([2,4]).T
        return plg.Polygon( pointMat)    
    
    def rectangle_to_polygon(rect):
        resBoxes=np.empty([1,8],dtype='int32')
        resBoxes[0,0]=int(rect.xmin)
        resBoxes[0,4]=int(rect.ymax)
        resBoxes[0,1]=int(rect.xmin)
        resBoxes[0,5]=int(rect.ymin)
        resBoxes[0,2]=int(rect.xmax)
        resBoxes[0,6]=int(rect.ymin)
        resBoxes[0,3]=int(rect.xmax)
        resBoxes[0,7]=int(rect.ymax)

        pointMat = resBoxes[0].reshape([2,4]).T
        
        return plg.Polygon( pointMat)
    
    def rectangle_to_points(rect):
        points = [int(rect.xmin), int(rect.ymax), int(rect.xmax), int(rect.ymax), int(rect.xmax), int(rect.ymin), int(rect.xmin), int(rect.ymin)]
        return points
    
    def get_intersection_over_gtRegions(pD,pG):
        try:
            return get_intersection(pD, pG) / pG.area();
        except:
            return 0

    def get_union(pD,pG):
        areaA = pD.area();
        areaB = pG.area();
        return areaA + areaB - get_intersection(pD, pG);
        
    def get_intersection_over_union(pD,pG):
        try:
            return get_intersection(pD, pG) / get_union(pD, pG);
        except:
            return 0
    
    def funcCt(x):
        if x<=0.01:
            return 1
        else:
            return 1-x

    
    def get_text_intersection_over_Gt_area_recall(pD, pG):
        '''
        Ct (cut): Area of ground truth that is not covered by detection bounding box.
        '''
        try:
            Ct = pG.area() - get_intersection(pD, pG)
            assert(Ct>=0 and Ct<=pG.area()), 'Invalid Ct value'
            assert(pG.area()>0), 'Invalid Gt'
            return (get_intersection(pD, pG) * funcCt(Ct*1.0/pG.area())) / pG.area(); #
        except Exception as e:
            print(e)
            return 0

    
    def get_text_intersection_over_union_recall(pD, pG):
        '''
        Ct (cut): Area of ground truth that is not covered by detection bounding box.
        '''
        try:
            Ct = pG.area() - get_intersection(pD, pG)
            assert(Ct>=0 and Ct<=pG.area()), 'Invalid Ct value'
            assert(pG.area()>0), 'Invalid Gt'
            return (get_intersection(pD, pG) * funcCt(Ct*1.0/pG.area())) / get_union(pD, pG);
        except Exception as e:
            print(e)
            return 0

    
    def funcOt(x):
        if x<=0.01:
            return 1
        else:
            return 1-x

    
    def get_text_intersection_over_union_precision(pD, pG, gtNum, gtPolys, gtDontCarePolsNum):
        '''
        Ot (Outlier gt area)
        '''
        Ot = 0
        try:
            inside_pG = pD & pG
            gt_union_inside_pD = None
            gt_union_inside_pD_and_pG = None
            count_initial = 0
            for i in xrange(len(gtPolys)):
                if i!= gtNum and gtNum not in gtDontCarePolsNum: # ignore don't care regions
                    if not get_intersection(pD, gtPolys[i]) == 0:
                        if count_initial == 0:
                            # initial 
                            gt_union_inside_pD = gtPolys[i]
                            gt_union_inside_pD_and_pG = inside_pG & gtPolys[i]
                            count_initial = 1
                            continue
                        gt_union_inside_pD = gt_union_inside_pD | gtPolys[i]
                        inside_pG_i = inside_pG & gtPolys[i]
                        gt_union_inside_pD_and_pG = gt_union_inside_pD_and_pG | inside_pG_i

            if not gt_union_inside_pD == None:
                pD_union_with_other_gt = pD & gt_union_inside_pD
                Ot = pD_union_with_other_gt.area() - gt_union_inside_pD_and_pG.area()
                if Ot <=1.0e-10:
                    Ot = 0
            else:
                Ot = 0
            assert(Ot>=0 and Ot<=pD.area()+0.001), 'Invalid Ot value: '+str(Ot)+' '+str(pD.area())
            assert(pD.area()>0), 'Invalid pD: '+str(pD.area())
            return (get_intersection(pD, pG) * funcOt(Ot*1.0/pD.area())) / get_union(pD, pG);
        except Exception as e:
            print(Ot, pD.area())
            print(e)
            return 0


    def get_intersection(pD,pG):
        pInt = pD & pG
        if len(pInt) == 0:
            return 0
        return pInt.area()

    
    def get_intersection_three(pD,pG,pGi):
        pInt = pD & pG
        pInt_3 = pInt & pGi
        if len(pInt_3) == 0:
            return 0
        return pInt_3.area()
    
    def compute_ap(confList, matchList,numGtCare):
        correct = 0
        AP = 0
        if len(confList)>0:
            confList = np.array(confList)
            matchList = np.array(matchList)
            sorted_ind = np.argsort(-confList)
            confList = confList[sorted_ind]
            matchList = matchList[sorted_ind]
            for n in range(len(confList)):
                match = matchList[n]
                if match:
                    correct += 1
                    AP += float(correct)/(n + 1)

            if numGtCare>0:
                AP /= numGtCare
            
        return AP
    
    perSampleMetrics = {}
    
    matchedSum = 0
    matchedSum_iou = 0 
    matchedSum_tiouGt = 0 
    matchedSum_tiouDt = 0 
    matchedSum_cutGt = 0 
    matchedSum_coverOtherGt = 0 
    
    Rectangle = namedtuple('Rectangle', 'xmin ymin xmax ymax')
    
    gt = rrc_evaluation_funcs.load_zip_file(gtFilePath,evaluationParams['GT_SAMPLE_NAME_2_ID'])
    subm = rrc_evaluation_funcs.load_zip_file(submFilePath,evaluationParams['DET_SAMPLE_NAME_2_ID'],True)
    gt_tl = rrc_evaluation_funcs.load_zip_file(gtTextLineFilePath,evaluationParams['GT_SAMPLE_NAME_2_ID'])

    numGlobalCareGt = 0;
    numGlobalCareDet = 0;
    
    arrGlobalConfidences = [];
    arrGlobalMatches = [];

    totalNumGtPols = 0
    totalNumDetPols = 0

    for index_gt, resFile in enumerate(gt):
        gtFile = rrc_evaluation_funcs.decode_utf8(gt[resFile])
        gt_tlFile = rrc_evaluation_funcs.decode_utf8(gt_tl[resFile])
        recall = 0
        precision = 0
        hmean = 0    
        
        detMatched = 0
        detMatched_iou = 0 
        detMatched_tiouGt = 0 
        detMatched_tiouDt = 0 
        
        iouMat = np.empty([1,1])
        
        gtPols = []
        detPols = []
        gt_tlPols = []
        
        gtPolPoints = []
        detPolPoints = []  
        gt_tlPolPoints = []
        
        #Array of Ground Truth Polygons' keys marked as don't Care
        gtDontCarePolsNum = []
        valid_gtDontCare = 0
        #Array of Detected Polygons' matched with a don't Care GT
        detDontCarePolsNum = []   
        gt_tlDontCarePolsNum = []
        
        pairs = []
        detMatchedNums = []
        tl_pairs = []
        
        arrSampleConfidences = [];
        arrSampleMatch = [];
        sampleAP = 0;

        evaluationLog = ""

        pointsList,_,transcriptionsList = rrc_evaluation_funcs.get_tl_line_values_from_file_contents(gtFile,evaluationParams['CRLF'],evaluationParams['LTRB'],True,False)
        tl_pointsList,_,tl_transcriptionsList = rrc_evaluation_funcs.get_tl_line_values_from_file_contents(gt_tlFile,evaluationParams['CRLF'],evaluationParams['LTRB'],True,False)

        for n in range(len(pointsList)):
            points = pointsList[n]
            transcription = transcriptionsList[n]
            dontCare = transcription == "###"
            if evaluationParams['LTRB']:
                gtRect = Rectangle(*points)
                gtPol = rectangle_to_polygon(gtRect)
            else:
                gtPol = polygon_from_points(points)
            gtPols.append(gtPol)
            gtPolPoints.append(points)
            if dontCare:
                gtDontCarePolsNum.append( len(gtPols)-1 ) 
        for n in range(len(tl_pointsList)):
            tl_points = tl_pointsList[n]
            if evaluationParams['LTRB']:
                gt_tlRect = Rectangle(*tl_points)
                gt_tlPol = rectangle_to_polygon(gt_tlRect)
            else:
                gt_tlPol = polygon_from_points(tl_points)
            gt_tlPols.append(gt_tlPol)
            gt_tlPolPoints.append(tl_points)

        evaluationLog += "GT polygons: " + str(len(gtPols)) + " GT-Textline polygons: " + str(len(gt_tlPols)) + (" (" + str(len(gtDontCarePolsNum)) + " don't care)\n" if len(gtDontCarePolsNum)>0 else "\n")
        if resFile in subm:
            
            detFile = rrc_evaluation_funcs.decode_utf8(subm[resFile]) 
            
            pointsList,confidencesList,_ = rrc_evaluation_funcs.get_tl_line_values_from_file_contents(detFile,evaluationParams['CRLF'],evaluationParams['LTRB'],False,evaluationParams['CONFIDENCES'])
            for n in range(len(pointsList)):
                points = pointsList[n]
                
                if evaluationParams['LTRB']:
                    detRect = Rectangle(*points)
                    detPol = rectangle_to_polygon(detRect)
                else:
                    detPol = polygon_from_points(points)                    
                detPols.append(detPol)
                detPolPoints.append(points)
                if len(gtDontCarePolsNum)>0 :
                    for dontCarePol in gtDontCarePolsNum:
                        dontCarePol = gtPols[dontCarePol]
                        intersected_area = get_intersection(dontCarePol,detPol)
                        pdDimensions = detPol.area()
                        precision = 0 if pdDimensions == 0 else intersected_area / pdDimensions
                        if (precision > evaluationParams['AREA_PRECISION_CONSTRAINT'] ):
                            detDontCarePolsNum.append( len(detPols)-1 )
                            break
                                
            evaluationLog += "DET polygons: " + str(len(detPols)) + (" (" + str(len(detDontCarePolsNum)) + " don't care)\n" if len(detDontCarePolsNum)>0 else "\n")
            
            if len(gtPols)>0 and len(detPols)>0:
                #Calculate IoU and precision matrixs
                outputShape=[len(gtPols),len(detPols)]
                iouMat = np.empty(outputShape)
                gtRectMat = np.zeros(len(gtPols),np.int8)
                gttlRectMat = np.zeros(len(gt_tlPols),np.int8)
                detRectMat = np.zeros(len(detPols),np.int8)
                tiouRecallMat = np.empty(outputShape)  
                tiouPrecisionMat = np.empty(outputShape)  
                tiouGtRectMat = np.zeros(len(gtPols),np.int8) 
                tiouDetRectMat = np.zeros(len(detPols),np.int8) 

                ioGt_Mat = np.zeros(outputShape)
                area_tiouRecallMat = np.zeros(outputShape)
                # text-line evaluation is calculated in advance. 
                gt_and_gt_tl_outputShape=[len(gt_tlPols), len(gtPols)]
                gt_and_gt_tl_Mat = np.zeros(gt_and_gt_tl_outputShape)
                tl_outputShape=[len(gt_tlPols),len(detPols)]
                tl_iouMat = np.zeros(tl_outputShape)

                tl_tiouPrecisionMat = np.zeros(tl_outputShape)  
                tl_tiouGtRectMat = np.zeros(len(gt_tlPols),np.int8) 
                tl_tiouDetRectMat = np.zeros(len(detPols),np.int8) 

                for gt_tlNum in range(len(gt_tlPols)): # 
                    for gt_Num in range(len(gtPols)):
                        gt_and_gt_tl_Mat[gt_tlNum,gt_Num] = get_intersection_over_gtRegions(gt_tlPols[gt_tlNum],gtPols[gt_Num])

                gt_gt_tl_Matching_index = np.where(gt_and_gt_tl_Mat >= 0.5)

                for gtNum in range(len(gtPols)):
                    for detNum in range(len(detPols)):
                        pG = gtPols[gtNum]
                        pD = detPols[detNum]
                        iouMat[gtNum,detNum] = get_intersection_over_union(pD,pG)
                        tiouRecallMat[gtNum,detNum] = get_text_intersection_over_union_recall(pD,pG)  
                        tiouPrecisionMat[gtNum,detNum] = get_text_intersection_over_union_precision(pD, pG, gtNum, gtPols, gtDontCarePolsNum)  
                        ioGt_Mat[gtNum,detNum] = get_intersection_over_gtRegions(pD,pG)
                        area_tiouRecallMat[gtNum,detNum] = get_text_intersection_over_Gt_area_recall(pD,pG)  

                for gt_tlNum in range(len(gt_tlPols)):
                    for detNum in range(len(detPols)):
                        pG = gt_tlPols[gt_tlNum]
                        pD = detPols[detNum]
                        tl_iouMat[gt_tlNum,detNum] = get_intersection_over_union(pD,pG)
                        tl_tiouPrecisionMat[gt_tlNum,detNum] = get_text_intersection_over_union_precision(pD, pG, gt_tlNum, gtPols, [])  

                        if gttlRectMat[gt_tlNum] == 0 and detRectMat[detNum] == 0 and detNum not in detDontCarePolsNum:
                            if tl_iouMat[gt_tlNum,detNum]>evaluationParams['IOU_CONSTRAINT']:
                                detRectMat[detNum] = 1
                                gttlRectMat[gt_tlNum] = 1
                                detMatched += 1
                                detMatched_tiouDt += tl_tiouPrecisionMat[gt_tlNum,detNum] 
                                # ---- WordMatchTl
                                wmtl = gt_gt_tl_Matching_index[1][np.where(gt_gt_tl_Matching_index[0] == gt_tlNum)[0]]
                                for w2tl_index in wmtl:
                                    if ioGt_Mat[w2tl_index, detNum]>0.5:
                                        gtRectMat[w2tl_index] = 1
                                        gtDontCarePolsNum.append(w2tl_index)
                                        valid_gtDontCare += 1
                                        if len(wmtl)>=2: # Normally, each TL annotation should contain at least two gt from WL annotations. 
                                            detMatched_tiouGt += area_tiouRecallMat[w2tl_index,detNum] 
                                        else: 
                                            detMatched_tiouGt += tiouRecallMat[w2tl_index,detNum] # same as OO match.

                                tl_pairs.append({'gt_tl':gt_tlNum,'det':detNum})
                                detMatchedNums.append(detNum)
                                evaluationLog += "Match GT #" + str(gt_tlNum) + " with Det #" + str(detNum) + "\n"

                if len(gtDontCarePolsNum)>0: # ---- redefined.
                    for dontCarePolStage2 in gtDontCarePolsNum:
                        for detNum in range(len(detPols)):
                            if detRectMat[detNum] == 0 and detNum not in detDontCarePolsNum:
                                detPol = detPols[detNum]
                                plgStage2 = gtPols[dontCarePolStage2]
                                intersected_area = get_intersection(plgStage2,detPol)
                                pdDimensions = detPol.area()
                                precision = 0 if pdDimensions == 0 else intersected_area / pdDimensions
                                if (precision > evaluationParams['AREA_PRECISION_CONSTRAINT']):
                                    detDontCarePolsNum.append(detNum)
                                    break

                for gtNum in range(len(gtPols)):
                    for detNum in range(len(detPols)):
                        if gtRectMat[gtNum] == 0 and detRectMat[detNum] == 0 and gtNum not in gtDontCarePolsNum and detNum not in detDontCarePolsNum:
                            if iouMat[gtNum,detNum]>evaluationParams['IOU_CONSTRAINT']:
                                gtRectMat[gtNum] = 1
                                detRectMat[detNum] = 1
                                detMatched += 1
                                detMatched_tiouGt += tiouRecallMat[gtNum,detNum] 
                                detMatched_tiouDt += tiouPrecisionMat[gtNum,detNum] 
                                pairs.append({'gt':gtNum,'det':detNum})
                                detMatchedNums.append(detNum)
                                evaluationLog += "Match GT #" + str(gtNum) + " with Det #" + str(detNum) + "\n"

            if evaluationParams['CONFIDENCES']:
                for detNum in range(len(detPols)):
                    if detNum not in detDontCarePolsNum :
                        #we exclude the don't care detections
                        match = detNum in detMatchedNums

                        arrSampleConfidences.append(confidencesList[detNum])
                        arrSampleMatch.append(match)

                        arrGlobalConfidences.append(confidencesList[detNum]);
                        arrGlobalMatches.append(match);

        numGtCare = (len(gtPols) - len(gtDontCarePolsNum) + valid_gtDontCare)
        numDetCare = (len(detPols) - len(detDontCarePolsNum))
        if numGtCare == 0:
            recall = float(1)
            precision = float(0) if numDetCare >0 else float(1)
            sampleAP = precision
            tiouRecall = float(1) 
            tiouPrecision = float(0) if numDetCare >0 else float(1) 
        else:
            recall = float(detMatched) / numGtCare
            precision = 0 if numDetCare==0 else float(detMatched) / numDetCare
            tiouRecall = float(detMatched_tiouGt) / numGtCare 
            tiouPrecision = 0 if numDetCare==0 else float(detMatched_tiouDt) / numDetCare 

            if evaluationParams['CONFIDENCES'] and evaluationParams['PER_SAMPLE_RESULTS']:
                sampleAP = compute_ap(arrSampleConfidences, arrSampleMatch, numGtCare )                    

        hmean = 0 if (precision + recall)==0 else 2.0 * precision * recall / (precision + recall)
        tiouHmean = 0 if (tiouPrecision + tiouRecall)==0 else 2.0 * tiouPrecision * tiouRecall / (tiouPrecision + tiouRecall)     

        matchedSum += detMatched
        matchedSum_tiouGt += detMatched_tiouGt 
        matchedSum_tiouDt += detMatched_tiouDt 
        numGlobalCareGt += numGtCare
        numGlobalCareDet += numDetCare
        
        if evaluationParams['PER_SAMPLE_RESULTS']:
            perSampleMetrics[resFile] = {
                                            'precision':precision,
                                            'recall':recall,
                                            'hmean':hmean,
                                            'tiouPrecision':tiouPrecision,
                                            'tiouRecall':tiouRecall,
                                            'tiouHmean':tiouHmean,
                                            'pairs':pairs,
                                            'AP':sampleAP,
                                            'iouMat':[] if len(detPols)>100 else iouMat.tolist(),
                                            'gtPolPoints':gtPolPoints,
                                            'detPolPoints':detPolPoints,
                                            'gtDontCare':gtDontCarePolsNum,
                                            'detDontCare':detDontCarePolsNum,
                                            'evaluationParams': evaluationParams,
                                            'evaluationLog': evaluationLog                                        
                                        }
        try:
            totalNumGtPols += len(gtPols) 
            totalNumDetPols += len(detPols)
        except Exception as e:
            raise e

    AP = 0
    if evaluationParams['CONFIDENCES']:
        AP = compute_ap(arrGlobalConfidences, arrGlobalMatches, numGlobalCareGt)

    print('num_gt, num_det: ', numGlobalCareGt, totalNumDetPols)
    methodRecall = 0 if numGlobalCareGt == 0 else float(matchedSum)/numGlobalCareGt
    methodPrecision = 0 if numGlobalCareDet == 0 else float(matchedSum)/numGlobalCareDet
    methodHmean = 0 if methodRecall + methodPrecision==0 else 2* methodRecall * methodPrecision / (methodRecall + methodPrecision)

    methodRecall_tiouGt = 0 if numGlobalCareGt == 0 else float(matchedSum_tiouGt)/numGlobalCareGt 
    methodPrecision_tiouDt = 0 if numGlobalCareDet == 0 else float(matchedSum_tiouDt)/numGlobalCareDet 
    tiouMethodHmean = 0 if methodRecall_tiouGt + methodPrecision_tiouDt==0 else 2* methodRecall_tiouGt * methodPrecision_tiouDt / (methodRecall_tiouGt + methodPrecision_tiouDt) 
    
    methodMetrics = {'precision':methodPrecision, 'recall':methodRecall,'hmean': methodHmean}
    tiouMethodMetrics = {'tiouPrecision':methodPrecision_tiouDt, 'tiouRecall':methodRecall_tiouGt,'tiouHmean': tiouMethodHmean }
    print('Origin:')
    print("recall: ", round(methodRecall,3), "precision: ", round(methodPrecision,3), "hmean: ", round(methodHmean,3))
    print('tiouNewMetric:')
    print("tiouRecall:", round(methodRecall_tiouGt,3), "tiouPrecision:", round(methodPrecision_tiouDt,3), "tiouHmean:", round(tiouMethodHmean,3))
    
    resDict = {'calculated':True,'Message':'','method': methodMetrics,'per_sample': perSampleMetrics, 'tiouMethod': tiouMethodMetrics}
    
    return resDict;

if __name__=='__main__':
    rrc_evaluation_funcs.main_evaluation(None,default_evaluation_params,validate_data,evaluate_method)
