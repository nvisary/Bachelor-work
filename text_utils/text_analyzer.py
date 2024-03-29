import difflib, Levenshtein, distance
import numpy as np

def jacquard_coefficient(text1, text2):
    count_compare = 0
    for word in text1:
        for word2 in text2:
            word.lower()
            word2.lower()
            if word == word2:
                count_compare += 1
    a = len(text1) - 1
    b = len(text2) - 1
    return count_compare / (a + b - count_compare)


def get_levenshtein(text1, text2):
    if len(text1) == len(text2):
        ratios = []
        for i in range(len(text1)):
            ratios.append(Levenshtein.ratio(text1[i], text2[i]))
        return np.mean(ratios)
    return None


def text_compare(text_array1, text_array2):
    first_text_len = len(text_array1)
    second_text_len = len(text_array2)
    if first_text_len >= second_text_len:
        count_words = first_text_len
    else:
        count_words = second_text_len

    compare_words = []
    for i in range(count_words):
        first_word_len = 0
        second_word_len = 0

        if i < first_text_len:
            first_word_len = len(text_array1[i])

        if i < second_text_len:
            second_word_len = len(text_array2[i])

        if first_word_len >= second_word_len:
            count_letters = first_word_len
        else:
            count_letters = second_word_len

        compare_letters = []
        for j in range(count_letters):
            letter1 = 0
            letter2 = 0

            if j < first_word_len and i < first_text_len:
                letter1 = text_array1[i][j]
            if j < second_word_len and i < second_text_len:
                letter2 = text_array2[i][j]

            if letter1 == letter2:
                compare_letters.append(1)
            else:
                compare_letters.append(0)
        compare_words.append(sum(compare_letters) * 100 / count_letters)

    return sum(compare_words) / len(compare_words)


def levenshtein(word1, word2):
    return Levenshtein.ratio(word1, word2)


def compare(array, array2):
    if len(array) != len(array2):
        return 0
    lev = 0
    for i in range(len(array)):
        lev += levenshtein(array[i], array2[i])
    return lev / len(array)


a = """для американской литературы нехарактерные, но очень хорошо знакомые нам по литературе русской, и выделили ее 
из ряда современных романистов и философов. Большинство ее героев на первый взгляд вычерчены графично, 
почти в черно-белых тонах. Белым — творцы, герои; черным — паразиты, безликие ничтожества, черпающие силу в круговой 
поруке, в манипуляции сознанием, в мифах об изначальной греховности человека и его ничтожности по сравнению с высшей 
силой, будь то всемогущий Бог или столь же всемогущее государство, в морали жертвенности, самоуничижения, 
в возвеличивании страдания и, наконец, в насилии над всеми, кто выбивается из ряда. А что случится, 
если немногочисленные в каждом, даже самом демократическом обществе творцы вдруг однажды забастуют?Что делать, 
как создать новый, истинно человеческий мир, в котором хотелось бы жить каждой неповторимой личности? Этот вопрос и 
ставит Айн Рэнд. Что мы должны уяснить, чтобы почувствовать себя атлантами? Что нельзя жить заемной жизнью, 
заемными ценностями. Что можно и нужно изменять себя, но никогда не изменять себе. Что невозможно жить ради других 
или требовать, чтобы другие жили ради тебя. Что человек создан для счастья, но нельзя быть счастливым, 
ни руководствуясь чужими представлениями о счастье, ни за счет несчастья других, ни за счет незаслуженных благ. Нужно 
отвечать за свои действия и их последствия. Нельзя противопоставлять мораль и жизнь, духовное и материальное. 
Хваленый альтруизм в конечном счете неизменно оборачивается орудием порабощения человека человеком и только множит 
насилие и страдания. Но недостаточно принять эти принципы, надо жить в соответствии с ними, а это нелегко. Может 
быть, у Вас возникает желание резко осудить эгоистичную, безбожную, антигуманную позицию автора и ее «нормативных» 
героев?Что ж, реакция вполне понятная. Однако стоит задуматься, в чем истоки такой реакции. Уж не в том ли, 
что страшновато выйти из-под опеки Отца (который то ли на небе, то ли в Кремле, то ли по соседству в Мавзолее), 
наконец признать себя взрослым и самостоятельным, принять на себя ответственность за самые важные жизненные решения? 
Очень хочется поспорить с философом Айн Рэнд, русской родоначальницей американского объективизма, но не так-то просто 
опровергнуть ее впечатляющую логику. Так как же творить мир, в котором не противно жить? Думайте. Сами. Невзирая на 
авторитеты.Будем очень благодарны за Ваше мнение о книге и о поставленных в ней проблемах и за отзыв — даже 
критический. ЧАСТЬ ПЕРВАЯБЕЗ ПРОТИВОРЕЧИЙГлава 1Тема— Кто такой Джон Галт?Вопрос бродяги прозвучал вяло и 
невыразительно. В сгущавшихся сумерках было не рассмотреть его лица, но вот тусклые лучи заходящего солнца, 
долетевшие из глубины улицы, осветили смотревшие прямо на Эдди Виллерса безнадежно-насмешливые глаза — будто вопрос 
был задан не ему лично, а тому необъяснимому беспокойству, что затаилось в его душе.— С чего это ты вдруг спросил? — 
Голос Эдди Виллерса прозвучал довольно неприязненно.Бродяга стоял, прислонившись к дверному косяку, в осколке стекла 
за его спиной отражалось желтое, отливающее металлом небо.— А почему это вас беспокоит? — спросил он.— Да ничуть,
 — огрызнулся Эдди Виллерс. — Он поспешно сунул руку в карман. Бродяга остановил его и, попросив десять центов, 
начал говорить дальше, словно стремясь заполнить один неловкий момент и отдалить приближение другого. В последнее 
время попрошайничество на улице стало обычным делом, так что внимать каким-то объяснениям было совсем не обязательно, 
к тому же у Эдди не было никакого желания выслушивать, как именно этот бродяга докатился до такой жизни.— Вот возьми, 
купи себе чашку кофе. — Эдди протянул монету в сторону безликой тени.— Спасибо, сэр, — сказал бродяга равнодушным 
тоном. Он наклонился вперед, и Эдди рассмотрел изрезанное морщинами, обветренное лицо, на котором застыла печать 
усталости и циничного безразличия. У бродяги были глаза умного человека.Эдди Виллерс пошел дальше, пытаясь понять, 
почему с наступлением сумерек его всегда охватывает какой-то необъяснимый, беспричинный страх. Нет, даже не страх, 
ему было нечего бояться, просто непреодолимая смутная тревога, беспричинная и необъяснимая. Он давно привык к этому 
странному чувству, но не мог найти ему объяснения; и все же бродяга говорил с ним так, будто знал, что это чувство не 
давало ему покоя, будто считал, что оно должно возникать у каждого, более того, будто знал, почему это так.Эдди 
Виллерс расправил плечи, пытаясь привести мысли в порядок. «Пора с этим покончить», — подумал он; ему начинала 
мерещиться всякая чепуха. Неужели это чувство всегда преследовало его? Ему было тридцать два года. Он напряг память, 
пытаясь вспомнить. Нет, конечно же, не всегда, но он забыл, когда впервые ощутил его. Это чувство возникало внезапно, 
без всякой причины, но в последнее время значительно чаще, чем когда бы то ни было. «Это все из-за сумерек,
 — подумал Эдди, — терпеть их не могу».В сгущавшемся мраке тучи на небе и очертания строений становились едва 
различимыми, принимая коричневатый оттенок, — так, увядая, блекнут с годами краски на старинных холстах. Длинные 
потеки грязи, сползавшие с крыш высотных зданий, тянулись вниз по непрочным, покрытым копотью стенам. По стене одного 
из небоскребов протянулась трещина длиной в десять этажей, похожая на застывшую в момент вспышки молнию. Над крышами 
в небосвод вклинилось нечто кривое, с зазубренными краями. Это была половина шпиля, расцвеченная алым заревом заката,
 — со второй половины давно уже облезла позолота.Этот свет напоминал огромное, смутное опасение чего-то неведомого, 
исходившего неизвестно откуда, отблески пожара, но не бушующего, а затухающего, гасить который уже слишком 
поздно.«Нет, — думал Эдди Виллерс — город выглядит совершенно нормально, в его облике нет ничего зловещего».Эдди 
пошел дальше, напоминая себе, что опаздывает на работу. Он был далеко не в восторге от того, что ему там предстояло, 
но он должен был это сделать, поэтому решил не тянуть время и ускорил шаг.Он завернул за угол. Высоко над тротуаром в 
узком промежутке между темными силуэтами двух зданий, словно в проеме приоткрытой двери, он увидел табло гигантского 
календаря.Табло было установлено в прошлом году на крыше одного из домов по распоряжению мэра Нью-Йорка, чтобы жители 
города могли, подняв голову, сказать, какой сегодня день и месяц, с той же легкостью, как определить, который час, 
взглянув на часы; и теперь белый прямоугольник возвышался над городом, показывая прохожим месяц и число. В ржавых 
отблесках заката табло сообщало: второе сентября.Эдди Виллерс отвернулся. Ему никогда не нравился этот календарь. Он 
не мог понять, почему при виде его им овладевало странное беспокойство. Это ощущение имело что-то общее с тем 
чувством тревоги, которое преследовало его; оно было того же свойства.Ему вдруг показалось, что где-то он слышал 
фразу, своего рода присказку, которая передавала то, что, как казалось, выражал этот календарь. Но он забыл ее и шел 
по улице, пытаясь припомнить эти несколько слов, засевших в его сознании, словно образ, лишенный всякого содержания, 
который он не мог ни наполнить смыслом, ни выбросить из головы. Он оглянулся.Белый прямоугольник возвышался над 
крышами домов, глася с непреклонной категоричностью: второе сентября.Эдди Виллерс перевел взгляд вниз, на улицу, 
на ручную тележку зеленщика, стоявшую у крыльца сложенного из красного кирпича дома. Он увидел пучок золотистой 
моркови и свежую зелень молодого лука, опрятную белую занавеску, развевающуюся в открытом окне, и лихо заворачивающий 
за угол автобус. Он с удивлением отметил, что к нему вновь вернулись уверенность и спокойствие, и в то же время 
внезапно ощутил необъяснимое желание, чтобы все это было каким-то образом защищено, укрыто от нависающего пустого 
неба.Он шел по Пятой авеню, не сводя глаз с витрин. Он ничего не собирался покупать, ему просто нравилось 
рассматривать витрины с товарами — бесчисленными товарами, изготовленными человеком и предназначенными для человека. 
Он любовался оживленно-процветающей улицей, где, несмотря на поздний час, бурлила жизнь, и лишь немногие закрывшиеся 
магазины сиротливо смотрели на улицу темно — пустыми витринами.Эдди не знал, почему он вдруг вспомнил о дубе. Вокруг 
не было ничего, что могло бы вызвать это воспоминание. Но в его памяти всплыли и дуб, и дни летних каникул, 
проведенные в поместье мистера Таггарта. С детьми Таггартов Эдди провел большую часть своего детства, 
а сейчас работал на них, как его отец и дед работали в свое время на их отца и деда.Огромный дуб рос на холме у 
Гудзона в укромном уголке поместья Таггартов. Эдди Виллерс, которому тогда было семь лет, любил убегать, 
чтобы взглянуть на него.Дуб рос на этом месте уже несколько столетий, и Эдди думал, что он будет стоять здесь вечно. 
Глубоко вросшие в землю корни сжимали холм мертвой хваткой, и Эдди казалось, что если великан схватит дуб за верхушку 
и дернет что есть силы, то не сможет вырвать его с корнем, а лишь сорвет с места холм, а с ним и всю землю, 
и она повиснет на корнях дерева, словно шарик на веревочке. Стоя у этого дуба, он чувствовал себя в полной 
безопасности; в его представлении это было что-то неизменное, чему ничто не грозило. Дуб был для него величайшим 
символом силы.Однажды ночью в дуб ударила молния. Эдди увидел его на следующее утро. Дуб лежал на земле расколотый 
пополам, и при виде его изуродованного ствола Эдди показалось, что он смотрит на вход в огромный темный тоннель. 
Сердцевина дуба давно сгнила, превратившись в мелкую серую труху, которая разлеталась при малейшем дуновении ветра. 
Живительная сила покинула тело дерева, и то, что от него осталось, само по себе существовать уже не могло.Спустя 
много лет Эдди узнал, что детей нужно всячески оберегать от потрясений, что они должны как можно позже узнать, 
что такое смерть, боль и страх. Но его душу обожгло нечто другое: он пережил свое первое потрясение, когда стоял 
неподвижно, глядя на черную дыру, зиявшую в стволе сваленного молнией дерева. Это был страшный обман, 
еще более ужасный оттого, что Эдди не мог понять, в чем он заключался. Он знал, что обманули не его и не его веру, 
а что-то другое, но не понимал, что именно.Он постоял рядом с дубом, не проронив ни слова, и вернулся в дом. Он 
никогда никому об этом не рассказывал — ни в тот день, ни позже.Эдди с досадой мотнул головой и остановился у края 
тротуара, заметив, что светофор с ржавым металлическим скрежетом переключился на красный свет. Он сердился на себя. И 
с чего это он вдруг вспомнил сегодня про этот дуб? Дуб больше ничего для него не значил, от этого воспоминания 
остался лишь слабый привкус грусти и — где-то глубоко в душе — капелька боли, которая быстро исчезала, как исчезают, 
скатываясь вниз по оконному стеклу, капельки дождя, оставляя след, напоминающий вопросительный знак.Воспоминания 
детства были ему очень дороги, и он не хотел омрачать их грустью. В его памяти каждый день Детства был словно залит 
ярким, ровным солнечным светом, ему казалось, будто несколько солнечных лучей, даже не лучей, а точечек света, 
долетавших из тех далеких дней, временами придавали особую прелесть его работе, скрашивали одиночество его 
холостяцкой квартиры и оживляли монотонное однообразие его жизни.Эдди вспомнился один летний день, когда ему было 
девять лет. Он стоял посреди лесной просеки с лучшей подругой детства, и она рассказывала, что они будут делать, 
когда вырастут. Она говорила взволнованно, и слова ее были такими же беспощадно-ослепительными, как солнечный свет. """
b = " часть первая непротиворечие глава первая тема Кто такой Джон голт уже темнело и Ювелир не мог различить лица этого типа бродяга произнес четыре слова просто без выражения Однако далекий ответ ещё желтеет Шива заката отражался в его глазах и глаза эти смотрели на эти Уэльса как бы из насмешкой и вместе с тем невозмутимо словно вопрос был адресован не давшему его беспричинное беспокойство Почему ты спрашиваешь эйдемиллер встревожился бездельник стоял прислонясь плечом к дверной раме А почему тебя это волнует спросил он нисколько не волнует отрезал Эдди Уильямс он поспешно запустил руку в карман тип остановил его и profil одолжить 10 центов в последнее время на улицах столь часто попрошайничать что выслушивать объяснение было незачем ближе выпьешь кофе сказал иди Благодарю вас р ответил ему равнодушный Голос Дети willyrex отправил что дальше года я о том Почему в время суток он всегда испытывает беспричинный Ужас а Всегда ли с ним так было сейчас ему 32 я тебе попытался припомнить Нет не всегда Однако когда это началось он не сумел воспроизвести в памяти ощущение приходила к нему внезапно и Чайна но теперь приступы повторялись чаще чем когда-либо он шел напоминание себе на ходу что пора в контору то что он должен сделать После возвращения ему не нравилось Однако отлагательств не терпела он заставил себя поторопиться в узком пространстве между темными силуэтами двух зданий словно в щели при открывшейся двери иди уиллер увидел светящуюся в небе страничку гигантского календаря этот календарь мэр нью-йорка воздвиг в прошлом году на крыше небоскреба чтобы жители легко могли определить какой сегодня день белый прямоугольник парил над городом сообщает дату заполнивший улице людям в ржавом свете заката прямоугольника сообщал 2 сентября плюс отвернулся календарь раздражал его но почему сказать он не мог чувствует И перемешивалась песни давший его тревоги в них угадывалось иди перевел взгляд на улицу На тележку с овощами стоявшую дома из красного кирпича Он увидел грудью яркость золотистые моркови и свежие перья зеленого лука чистая белая занавеска плескалась на открытом окне за угол аккуратно заворачивать автобус дойдя до пятой Авеню он принялся рассматривать витрины магазинов видеть процветающую улицу всегда приятно уиллер удивился вернувшемуся чувство уверенности не знаю почему он вспомнил Летние дни проведённые в поместье Tager большая часть его детство прошло в компании детей тагиров а теперь он работал в корпорации как его дед и отец работали у Деда и отца так готов идти припомнил один из летних дней когда ему было 10 лет тогда на Лесной прогалине любимая подруга детства рассказывала ему о том что они будут делать когда вырастут он внимал ей с восхищением и удивлением и когда она спросила чем бы он хотел заниматься ответил без промедления надо совершить что-нибудь великое нам вдвоём и тут же добавил Пошли в воскресенье ещё не говорил что мы всегда должны искать себе лучшие А что по-твоему в нас лучшие она не ответила потому что глядела вдаль вдоль железнодорожной колеи петь delivers произнес эти слова 22 года назад и с тех пор они оставались для него аксиомой думай об этом Он подошел к огромному зданию таггерт трансконтинентал она была самым высоким и величественным на всей улице в длинных рядах окон ни одного разбитого в отличие от соседних домов контур здания вздымается вверх врезались в небо всякий раз входя в него он чувствовал облегчение и к нему возвращалась ощущение безопасности время от времени по стенам здания пробегала слабые дрожь поднимавшийся снизу из тоннелей огромного вокзала откуда поезда отправлялись через Континент и где они большой обратный путь из поколения в поколение от океана до океана так звучал гордый лозунг таггерт трансконтинентал от океана до океана и во веки веков подумал Эдди Уильямс шагая по безупречным коридором кабинету James таггарта президента тагертон Джеймс Джаггер оказался человеком которому уже почти исполнилось 50 у него были небольшой капризный рот Высокий лысеющий лоб облепленные с жидкими волосами бледное лицо с мягкими чертами и блеклый мутноватые глаза он выглядел уставшим и нездоровым ему было 39 лет с раздражением оглянулся на звук открывшейся двери не открывай не открывай не открывай меня Иди уиллер направился прямо к столу это важно Джем едим Уильямс посмотрел на карту висевшую Насти кабинета интересно Сколько президентов компании таггерд сидела под ней железные дороги таггерт трансконтинентал сеть красных линий от нью-йорка до сан-франциско напоминала систему кровеносных сосудов никогда в главном артерию в прыснули кровь и от избытка она стала разбегаться по всей стране разветвляется на случайные ручейки одна из красных дорожек таггерт трансконтинентал линия Revo норта проложила себе путь от шайенн вайоминг до эль-пасо в Техасе недавно добавилась новая ветка и красная полоса устремилась на юг за эль-пасо но de willyrex поспешно отвернулся когда глаза его коснулись этой точки посмотрев на Джеймса Tager то он сказал неприятности на линии Рио Норт новая крушение линия обречена нет смысла пускать пони поезда люди отказываются ездить в них на мой взгляд стране не найдётся ни одной железной дороге несколько веток которые не работали был убыток ну здесь не единственные в таком состоянии находится государство временно как Я полагаю как только мы проложим новую кальянную Jim новый Калине будет Я только что вернулся из контора этот Steel я разговаривал с чёрным морем зачем ты его побеспокоил первая партия рельсов должна поступить только в следующем месяце она должна была прийти 3 месяца назад непредвиденные обстоятельства абсолютно не зависящие от варана А первый срок поставки был назначен еще на полгода раньше Мы ждём интерес это Шейк ИТ Стил уже 13 месяцев не громким голосом насмешливое Осторожно таггерт осведомился И что же сказала моя сестрица она вернётся только завтра Ну и что по-твоему мне надо делать решать тебе но чтобы ты не сказал далее ты не Миша o'riordan Steel Gym Я не стану упоминать об этой компании Оренбург мой друг он поставить на материнскую при первой возможности и пока он не может этого сделать никто не вправе обменять на Jim Разве ты не понимаешь что-ли нереально разрушается внезависимости обвиняют нас в этом или нет нас непременно начнут обвинять даже без Феникс дурак и кто ещё не жаловался на ленивый Леонардо пока они не начали мутить воду Он заметил как напряглось лицо этим Gym Феникс дуранда работает просто прекрасная теперь он принадлежит и все грузовые перевозки резон нью-мексико и Колорадо мы не можем терять Колорадо Это наша последняя надежда если мы не соберёмся там Ступин пенис Дранга всех крупные грузоотправители штатам и так потеряли нефтяные месторождения уайатт так не понимаю почему все вокруг только и говорят нефтяных месторождениях во это Потому что я не сливает чудо сотвори сама это ведь не представилось месторождения которая занималась скалистый Пятачок в горах Колорадо и уже давно считалось выработанным и заброшенным отец и Лисова это выжимал из задыхающийся скважин скромный доход до конца своих дней а теперь словно бы кто-то в прыснул Адреналин В самое сердце горы и она забилась по-новому гоняя чёрную кровь нефть White Oil дала пустынным склонам новую жизнь новая города новые электростанции новые фабрики новый шины штат Там где раньше паслось несколько коров в огородах росла свекла это сделал 1 человек причём всего за 8 лет размышлял иди Уильямс ему хотелось познакомиться с элисом его и там говорили будто он обнаружил какой-то способ возрождать истощенные нефти на месторождения чем ты занимался по сию пору А ещё рассказывали что 33-летний Элис обладает буйным нравом пересылает жадный ублюдак Не интересующийся ничем кроме денег. Del James таггерт мы много лет весьма исправно обслуживали нефтяные месторождения бритомар старики убиваете мы отправляли состав цистерны раз в неделю сейчас не те времена Джин теннис дуранго отправляет оттуда два состава цистерн ежедневно и ходят они по расписанию Чего же он ожидает чтобы мы отказались от всех прочих отправителей жертвы интересы всей страны и предоставили ему все наши поезда он ничего не ждёт просто работает спиннинг дурак по-моему он беспринципный неразборчивый в средствах негодяй я вижу в нём безответственного выскочку Да знаю я знаю он делает деньги Мне кажется что не этим надлежит измерять пользу человека для общества а что касается Его нефти он приполз бык нам на коленях если бы не Феникс дурака Мы всегда категорически выступали против подобной хищнической конкуренции Но в данном случае мы бессильны и никто не винда чём ты какая разница куда соединять или нет Если дорога всё-равно разваливается Я ценю нашу детскую дружбу один но не забывай что президент таггерт трансконтинентал Пока ещё я идеал с привычно даже как-то равнодушна смотрел на него и спросил Так значит ты не собираешься делать что-либо для спасения Леонард и я этого не говорил как только заработаю трудники сан-себастьян и начнёт окупаться наши мексиканская давай ка давай не будем об этом твоя сестра сказала текст чёрту мою сестру стоял и смотрел прямо перед собой не замечая более Джеймса так это спустя мгновение он поклонился и вышел приемный фоп Харпер старший клерк ещё сидел за столом vertera чешки пол разобранный пишущей машинки он был главным клерком ещё у отца Джеймса Токката Харпер поднял глаза от машинки и посмотрел на эти Уиллиса вышедшего из кабинета президента мудрый и спокойный взгляд будто намекал что ему известно визит Иди в эту часть здания означало стена одно из веток равно какие-то что визит оказался бесплодным но папу харпера всё это было совершенно безразлично то же самое циничное безразличие Эдди виллерс видел и в глазах бродяги на уличном перекрёстке Что вы делаете спросил индюка на деталь пишущей машинки Проклятая штуковина снова сломалась послать в ремонт бесполезно в прошлый раз проводились 3 месяца Вот я их починить весом бесполезно иди повторил Том Харпер что бесполезно всё обсудить О чём ты папа я не собираюсь подавать заявку на приобретение новой пишущей машинки новые штампуют из жести и когда сдохнут старый придёт конец машинописным текстом сегодня в подземке была авария тормоза работать утром я не смог купить кабель от кашля аптека у нас на углу разорилась на прошлой неделе Железнодорожная компания Техас в прошлом месяце вчера закрыли на ремонт мост куинсборо О чём ты и вообще"

s1 = "не в этот ни"
s2 = "ни и этим ни"
'''print(levenshtein(s2, s1))

a = a.split()
b = b.split()
file_out = open("log.txt", "w")
for i in range(len(b)):
    print("i = [" + str(i) + "/" + str(len(b)) + "]")
    for j in range(len(a)):
        # print("j = [" + str(j) + "/" + str(len(a)) + "]")
        lev1 = levenshtein(a[j], b[i])
        if (j + 1) > len(a) - 1 or (i + 1) > len(b) - 1:
            break
        lev2 = levenshtein(a[j + 1], b[i + 1])
        flag = False
        lev = (lev1 + lev2) / 2
        if lev > 0.7:
            # file_out.write("LEV MORE THAN 0.5")
            if (j + 2) > len(a) - 1 or (i + 2) > len(b) - 1:
                break
            lev = levenshtein(a[j + 2], b[i + 2])
            if lev > 0.6:
                file_out.write(
                    str(lev) + " " + a[j] + " " + a[j + 1] + " " + a[j + 2] + " | " + b[i] + " " + b[i + 1] + " " + b[i + 2] + "\n")
        i += 1
        j += 1
    # print()
'''
