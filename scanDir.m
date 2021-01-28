function [files] = scanDir(root_dir)

files={};
if root_dir(end)~='/'
 root_dir=[root_dir,'/'];
end
fileList=dir(root_dir);  %扩展名
n=length(fileList);
cntpic=0;
for i=1:n
    if strcmp(fileList(i).name,'.')==1||strcmp(fileList(i).name,'..')==1
        continue;
    else
        fileList(i).name;
        if ~fileList(i).isdir % 如果不是目录则跳过
            
            full_name=[fileList(i).name]; % 这里选择要不要绝对路径
            
                 cntpic=cntpic+1;
                 files(cntpic)={full_name};
%              end
        else
            temp = scanDir([root_dir,fileList(i).name]);
            files = [files,temp];
        end
    end
end

end