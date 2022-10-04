# -*- coding: utf-8 -*-
#!/usr/bin/env python2
########################################################################################################################
# Имя модуля: Generator_Agent
# Назначение: Генерация случайных чисел для эмуляции отправки по протоколу UDP
#
# Версия интерпретатора: 2.7.15
# Автор: Дмитрий Ильюшкò ilyushko@itain.ru dm.ilyushko@gmail.com
# Создан: ??.12.2018
# Изменен: 04.04.2019
# Правообладатель:(c) ЗАО "Институт телекоммуникаций" www.itain.ru 2019
# Лицензия: MIT www.opensource.org/licenses/mit-license.php
########################################################################################################################
from __future__ import with_statement

from __future__ import absolute_import

import random
from io import open

def write():
    type = [1, 2, 3, 4, 5, 6, 7]
    chassis = [1, 2, 3, 4]
    module = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    port = [1, 2, 3, 4]

    print u"Generation random elements from lists: "  # t = random.choice(type)'
    t = 4

    print u"Type = " + unicode(t)

    c = random.choice(chassis)

    print u"chassis = " + unicode(c)

    m = random.choice(module)
    print u"module = " + unicode(m)

    p = random.choice(port)
    print u"ports = " + unicode(p)

    with open(u'init.conf', u'w') as f: f.write(unicode(t) + u" " + unicode(c) + u" " + unicode(m) + u" " + unicode(p))
