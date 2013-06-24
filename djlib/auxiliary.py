out=open("catalogue.py.new",'w')
for line in open("catalogue.py",'r'):
    if '[' in line and ']' in line:
        to_parse=line[line.index('[')+1:line.index(']')]
        start_line=line[:line.index('[')]
        to_write=start_line+'('+[(record.strip()[1:-1],record.strip()[1:-1]) for record in to_parse.split(',')].__str__()[1:-1]+')\n'
        out.write(to_write)
    else:
        out.write(line)
out.close()