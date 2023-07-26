import ConvertToSpeech
import string

def deleteDup(input_file):
    output_file = "noDup.txt"
    lines_seen = set()
    special_chars = set(string.punctuation)
    special_chars.add(' ')
    special_chars.add('\n')


    with open(input_file, 'r') as file_in:
        with open(output_file, 'w') as file_out:
            #unique=''
            for line in file_in:
                words = line.split()
                #unique_words = []
                unique =''
                for word in words:
                    if word not in lines_seen and word not in special_chars:
                        #unique_words.append(word)
                        unique+=word + ' '
                        lines_seen.add(word)
                #file_out.write(''.join(unique_words)+'\n')
                if unique!='':
                    unique+='\n'
                    file_out.write(unique)
    ConvertToSpeech.main('noDup.txt')

#mesk alhamaideh