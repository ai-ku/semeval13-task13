function runspectral(input_dir, out_dir)

addpath('../../bin/')
s = RandStream('mcg16807','Seed',0);
RandStream.setGlobalStream(s);

files = dir(input_dir);

for i=1:length(files)
    fname = files(i).name;
    if (~strcmp(fname, '.') && ~strcmp(fname, '..'))
        filename = [input_dir, '/', fname];
        cluster = 32; % take as an input? local/pos 
        sigma = 0;
        data = readsparse(['< cat ', filename], 100);
        tdata = data';
        sdata = max(tdata, data);
        clear tdata  data;
        dims = [2, 4, 8, 16, 32];
        [U , ~, ~] = sc(sdata, sigma, cluster);
        for i = 1:length(dims)
            out_fname = sprintf('%s.spectral.c%d', [out_dir, '/', fname], dims(i));
            fprintf(1, '%s\n', out_fname);
            V = U(:,1:dims(i));
            sq_sum = sqrt(sum(V.*V, 2)) + 1e-20;
            cluvec = V ./ repmat(sq_sum, 1, dims(i));
            dlmwrite(out_fname, cluvec, 'delimiter', '\t');
            pause(0.01);
        end
    end
    
end


exit;
end
