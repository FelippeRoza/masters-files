function [output] = readValue(s,command)
    % Serial send read request to Arduino
    fprintf(s,command);  

    % Read value returned via Serial communication 
    output = [0 0 0 0 0 0 0 0 toc];
    for i = 1:8
        output(i) = fscanf(s,'%f');
    end
end
