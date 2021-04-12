%% 按文件夹输入
data_set = [];
dirs = {'E:\ThMatlab\SVM\ecoli jm103\*.txt','E:\ThMatlab\SVM\ecoli kanr\*.txt'};
count = 0;
for d = dirs
    namelist = dir(d{1});%将数据所在文件夹导入，此时为一个struct
    for j = namelist'% 将struct转置，为后面输入数据做准备
        count = count+1;
        temp = load(fullfile(j.folder, j.name));% 相当于输入“绝对路径+文件名”
        data = temp(:,2)';% 取出强度，变为一行
        wave = temp(:,1);% 取出波数
        data_set(count,:) = data;% 将强度并为一个矩阵
    end
end
%% 设置训练集和测试集
jm = data_set(1:600,:);
kanr = data_set(601:1200,:);

train_set = zeros(200,526);
count = 0;
for i = {jm,kanr}
    T = i{1};
    S = size(T,1); 
    SampleRow = randperm(S); 
    SampleRows = SampleRow(1:100); 
    rand = T(SampleRows,:); 
    train_set(count*100+1:count*100+100,:) = rand;
    count = count+1;
end

labels = [zeros(100,1);ones(100,1)];
model = fitcsvm(train_set,labels,'BoxConstraint',10,'KernelFunction','linear');
predict_labels = predict(model,test_x);
accuracy = sum(test_y == predict_labels)/length(test_y);
fprintf('accuracy is :%.3f\n' ,accuracy);