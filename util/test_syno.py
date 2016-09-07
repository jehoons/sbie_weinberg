import getpass 
from sbie_weinberg.util import syno


def test_download():

    url = "http://143.248.32.25:5000"
    
    src = '/homes/jhsong/local/sbie_platform/code-with-inputdata.tar.gz' 
    
    dst_dir = '.'
    
    user = 'jhsong'

    print ("\nTo download dataset, you need to have password.")
    print ("If you do not know the password, then contact Je-hoon Song.")
    print ("email: song.jehoon@gmail.com\n")

    password = getpass.getpass()

    syno.download(url, src, dst_dir, user, password)


