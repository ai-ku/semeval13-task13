clc, clear
input_dir = '/home/tyr/playground/task13/run/trial/word/gap/';
files = dir(input_dir);
format long

num_clusters = 3:10; % there are 3-22 senses in test data.
num_reference_bootstraps = 10;

%Test different runs of k-means clustering
% iterations_test
iter_test = 5;
opt_index = zeros(iter_test, 1);
max_gap = zeros(iter_test, 1);

for i=3:length(files)
    tic
    fname = files(i).name;
    data = csvread([input_dir, fname]);
    
    for ii = 1:iter_test
        [ opt_index(ii), max_gap(ii)] = gap_statistics(data, num_clusters, ...
            num_reference_bootstraps);
    end   
    str = sprintf('%s %d %d %d %d %d', fname, round(mean(opt_index)), ...
        median(opt_index), round(mean(max_gap)), median(max_gap), ...
        (median(opt_index) + median(max_gap) / 2));
    disp(str);
    toc
end

%exit();