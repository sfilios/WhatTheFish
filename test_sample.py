import  unified

#here you want to test that you are actually returning the pretrained model
def test_get_model():
    assert unified.get_model()

#here you want to test that you are making predictions
def test_predictor():
    guess =  unified.predictor(1,1,1,1,1,1,1,1)
    assert type(guess) != None

#test if the predictions are actually correct
