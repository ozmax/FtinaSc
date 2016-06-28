# -*- coding: UTF-8 -*-

from ftina import FtinaPotaSc

fp = FtinaPotaSc("http://www.ftinapota.gr/places/all")
fp.get_categories()

places_to_links = fp.get_category_links(fp.places)
categories_to_links = fp.get_category_links(fp.categories)
#happyhour_to_links = fp.get_category_links(fp.happy_hour)

with open('ftina_data.txt', 'w') as f:
    f.write('Ανά περιοχή\n')
    for key, lst in places_to_links.iteritems():
        f.write('Περιοχή: {}\n\n'.format(key.encode('utf-8')))
        for item in lst:
            info = fp.get_single_info(item)
            fields = ['name', 'address', 'website', 
                      'telephone', 'prices']
            for field in fields:
                if field in info:
                    if field == 'prices':
                        for drink in info[field]:
                            for name, prices in drink.iteritems():
                                f.write('\t\t'+name.encode('utf-8')+
                                        ' '+prices[0].encode('utf-8')+
                                        ' '+prices[1].encode('utf-8')+'\n')
                        f.write('\n')
                    else:
                        f.write('\t{}: {}\n'.format(field, info[field].encode('utf-8')))
                    
        f.write(10*'*'+'\n\n')
    f.write(10*'='+'\n\n')
    f.write('Ανά κατηγορία μαγαζιού\n')
    for key, lst in categories_to_links.iteritems():
        f.write('Κατηγορία: {}\n\n'.format(key.encode('utf-8')))
        for item in lst:
            info = fp.get_single_info(item)
            fields = ['name', 'address', 'website', 
                      'telephone', 'prices']
            for field in fields:
                if field in info:
                    if field == 'prices':
                        for drink in info[field]:
                            for name, prices in drink.iteritems():
                                f.write('\t\t'+name.encode('utf-8')+
                                        ' '+prices[0].encode('utf-8')+
                                        ' '+prices[1].encode('utf-8')+'\n')
                        f.write('\n')
                    else:
                        f.write('\t{}: {}\n'.format(field, info[field].encode('utf-8')))
                    
        f.write(10*'*'+'\n\n')
    f.write(10*'='+'\n')

    
