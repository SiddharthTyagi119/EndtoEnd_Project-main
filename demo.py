#batch prediction
#training pipeline

from Insurance.pipeline.batch_prediction import start_batch_prediction
from Insurance.pipeline.training_pipeline import start_training_pipeline

file_path=r"E:\Data science\Projects\InsuranceProject\insurance.csv"
print(__name__)
if __name__=="__main__":
    try:
        #start batch prediction
        #output_file = start_batch_prediction(input_file_path=file_path)
        #print(output_file)
        #start training pipeline
        output = start_training_pipeline()
        #print(output)
        
    except Exception as e:
        print(e) 