# partition1.py
from urlnet.urltree import UrlTree
net = UrlTree()
net.BuildUrlTree('http://www.southwindpress.com')
fd = open('partition1.paj','w')
net.WritePajekStream('partition1',fd)
net.WritePajekPartitionFromPropertyValueLookup(fd,
                                               'anotherURLLevelsPartition',
                                               'level')
net.WritePajekPartitionFromPropertyValueLookup(fd,
                                               'anotherDomainLevelsPartition',
                                               'level',
                                               doDomains=True)
# make a test dictionary, which will turn into partitions numbered level+1000: 1000-1003
# this is useful solely for testing purposes.
dict = {0:1000,1:1001,2:1002,3:1003,}
net.WritePajekPartitionFromPropertyDict(fd,
                                               'YetAnotherURLLevelsPartition',
                                               'level',
                                               dict)
net.WritePajekPartitionFromPropertyDict(fd,
                                               'YetAnotherDomainLevelsPartition',
                                               'level',
                                               dict,
                                               doDomains=True)
fd.close()
