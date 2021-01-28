clear;
clc;
%% hyper parameters
germs = {'Chryseo', 'E25922', 'EF29212', 'PA27853', 'SA29213', 'Salmonella'};
[~, class_num] = size(germs);
Path = 'D:\pythonProject\Data\CL\20201114 pathogen classification\';

%% scan dir
outputs = [];
FeaturesSet = [0];
figure;
for i = 1:class_num
    FilePath = [Path char(germs(i))];
    FileNames = scanDir(FilePath); 
%% load spectra&cut out fingerprint region
    data_set = [];
    for j = FileNames
        data = importdata([FilePath '\' char(j)]); 
        wave = data(39:264, 1); %39—264 corresponding to 600-1800 cm-1
        data = data(39:264, 2); 
        data = zscore(data); % Z-score
        data_set = [data_set; data'];
    end
%% remove the baseline&label
    data_set = airPLS(data_set, 10e7, 3); % remove baseline
%% visualize
    subplot(class_num,1, i);
    plot(wave, mean(data_set, 1));
    title(char(germs(i)));
    axis([600, 1800, 0, 4.5]);
%% concatenate dataset
    [m, ~] = size(data_set);
    data_set = [data_set ones(m, 1)*(i-1)];
    fprintf('%s contains %d spectra\n', char(germs(i)), m);
    FeaturesSet = [FeaturesSet m];
    outputs = [outputs; data_set];
end
%% output dataset
dlmwrite([Path 'temp_dataset.txt'], outputs, 'delimiter', '\t');
dlmwrite([Path 'wave.txt'], wave, 'delimiter', '\t');
dlmwrite([Path 'features_set.txt'],FeaturesSet,  'delimiter', '\t');
